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
        </div>
      </div>
      <div class="col-md-1 col-md-offset-5">
          <button class="btn btn-primary" type="button" v-on:click.stop.prevent="back()">返回</button>
      </div>
    </div>

    <hr>
    <div id='json-content' conf-id="{{$route.params.conf_id}}"></div>
  </div>
</template>
<script>
  import "jquery-highlight";
  import "jquery-jsonview";
  import "../jquery.link";
  import config from 'config';

  export default {
    data() {
      return {
        confInfo: {}
      }
    },

    methods: {
      back() {
        this.$router.go({name: 'index'});
      },

      toggle_highlight(event) {
        let value = $('.highlight-kw').val();
        let status = $(event.toElement).attr('status');
        let jsonContentEle = $('#json-content');

        if (status === '0') {
          jsonContentEle.highlight(value);
          $(event.toElement).attr('status', '1');
        } else {
          jsonContentEle.unhighlight(value);
          $(event.toElement).attr('status', '0');
        }
      },

      toggleBtn() {
        $('#json-content').JSONView('toggle');
      }
    },

    ready() {
      let self = this;
      let jsonContentEle = $('#json-content');
      let conf_id = jsonContentEle.attr('conf-id');

      $.ajax({
        url: config.baseUrl + '/parse/conf/' + conf_id ,
        method: 'GET',
        success(data) {
          // 文件信息
          self.confInfo = data.file_info;
          jsonContentEle.JSONView(data.json);

          setTimeout(function(){
            // 为内容中的yunba.io的机器添加链接, 第二个参数为link的 href
            jsonContentEle.link('a\\w+-[\\w]+-[\\w]+', "#!/?no_cache=1&kw=");

            // 如果关键字为空就没必要高亮
            let value = $('.highlight-kw').val();
            if (value) {
              $('#highlight-toggle').trigger('click');
            }
          }, 500)

        },
        error(error) {
          alert(JSON.stringify(error));
        }
      });
    }

  }
</script>
