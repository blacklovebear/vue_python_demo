<style>
    .highlight {
      background-color: yellow
    }
    .conf-explain{
      margin-left: 50px;
    }
</style>
<template>
    <div>
      <!-- Example row of columns -->
      <h2 class="sub-header" style="display:inline-block">配置文件详情</h2>
      <span class="conf-explain">
        主机：{{confInfo.host_domain}} 文件路径：{{confInfo.conf_file_path}}
      </span>

      <div class="row">

        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control highlight-kw" placeholder="高亮关键字" value="{{$route.query.kw}}">
            <span class="input-group-btn">
              <button class="btn btn-default" id="highlight-toggle" type="button" status="0"
                      v-on:click.stop.prevent="toggle_highlight($event)">高亮/取消</button>
            </span>
          </div><!-- /input-group -->

        </div><!-- /.col-md-6 -->
        <div class="col-md-2 col-md-offset-5">
            <button class="btn btn-primary" type="button"
                      v-on:click.stop.prevent="loadFileContent($route.params.conf_id)">重新加载配置文件</button>
        </div>

        <div class="col-md-1">
            <button class="btn btn-primary" type="button"
                      v-on:click.stop.prevent="back()">返回</button>
        </div>

      </div>

      <hr>
      <div>{{fileLoadResult.message}}</div>
      <pre id="conf-detail" conf-id="{{$route.params.conf_id}}">{{confInfo.conf_content}}</pre>
    </div>
</template>
<script>

  import "jquery-highlight";
  import config from 'config';

  module.exports = {
    data: function(){
      return {
        confInfo: {},
        fileLoadResult:{},
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
          $('#conf-detail').highlight(value);
          $(event.toElement).attr('status', '1');
        } else {
          $('#conf-detail').unhighlight(value);
          $(event.toElement).attr('status', '0');
        }
      },

      // 将文件内容从机器上加载到数据库
      loadFileContent: function(conf_id){
        $.ajax({
          url: config.baseUrl + '/load/conf/' + conf_id ,
          method: 'GET',
          success: function(data){
            console.log(data);
            alert(data.message)
          },
          error: function(error){
            alert(JSON.stringify(error));
          }
        });
      }

    },

    ready: function () {
      var self = this;
      var conf_id = $('#conf-detail').attr('conf-id');
      $.ajax({
        url: config.baseUrl + '/confs/' + conf_id ,
        method: 'GET',
        success: function(data){
          self.confInfo = data.data;
          self.fileLoadResult = data.load_result;

          setTimeout(function(){
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
