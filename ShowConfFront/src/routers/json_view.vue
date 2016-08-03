<style scoped>
    @import '/node_modules/jquery-jsonview/dist/jquery.jsonview.css';
    @import '../styles/highlight.css';
    .conf-explain{
      margin-left: 50px;
    }
</style>
<template>
    <div>
      <h2 class="sub-header" style="display:inline-block">json格式的配置文件</h2>
      <span class="conf-explain">主机：{{confInfo.host_domain}} 文件路径：{{confInfo.conf_file_path}}</span>

      <div class="row">
        <div class="col-md-6">
          <div class="input-group">
            <input type="text" class="form-control highlight-kw" placeholder="高亮关键字" value="{{$route.query.kw}}">
            <span class="input-group-btn">
              <button class="btn btn-default" id="highlight-toggle" type="button" status="0" v-on:click.stop.prevent="toggle_highlight($event)">高亮/取消</button>
              <button class="btn btn-default" type="button" v-on:click.stop.prevent="toggleBtn()">展开/折叠</button>
            </span>
          </div><!-- /input-group -->
        </div><!-- /.col-md-6 -->

        <div class="col-md-1 col-md-offset-5">
            <button class="btn btn-primary" type="button"
                      v-on:click.stop.prevent="back()">返回</button>
        </div>
      </div><!-- /.row -->


      <hr>
      <div id='json-content' conf-id="{{$route.params.conf_id}}"></div>
    </div>
</template>
<script>
  import "jquery-highlight";
  import "jquery-jsonview";

  import "../jquery.link";
  import config from 'config';

  module.exports = {
    data: function(){
      return {
        confInfo: {}
      }
    },

    methods: {
      back: function(){
        this.$router.go({name: 'index'});
      },
      toggle_highlight: function(event){
        var value = $('.highlight-kw').val();
        var status = $(event.toElement).attr('status');
        if (status === '0') {
          $('#json-content').highlight(value);
          // $('#json-content').link(value);
          $(event.toElement).attr('status', '1');
        } else {
          $('#json-content').unhighlight(value);
          // $('#json-content').unlink(value);
          $(event.toElement).attr('status', '0');
        }
      },

      toggleBtn:function(){
        $('#json-content').JSONView('toggle');
      }
    },

    ready: function () {
      var self = this;
      var conf_id = $('#json-content').attr('conf-id');
      $.ajax({
        url: config.baseUrl + '/parse/conf/' + conf_id ,
        method: 'GET',
        success: function(data){
          // 文件信息
          self.confInfo = data.file_info;

          $('#json-content').JSONView(data.json);

          setTimeout(function(){

            // 为内容中的yunba.io的机器添加链接, 第二个参数为link的 href
            $('#json-content').link('a\\w+-[\\w]+-[\\w]+', "#!/index?no_cache=1&kw=");

            // 如果关键字为空就没必要高亮
            var value = $('.highlight-kw').val();
            if (value) {
              $('#highlight-toggle').trigger('click');
            }
          }, 500)

        },
        error: function(error){
          alert(JSON.stringify(error));
        }
      });
    }


  }
</script>
