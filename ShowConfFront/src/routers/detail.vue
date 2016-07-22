<style>
    .highlight {
      background-color: yellow
    }
</style>
<template>
    <div>
      <!-- Example row of columns -->
      <h2 class="sub-header" style="display:inline-block">配置文件详情</h2>
      <b>(主机：{{confInfo.host_domain}} 文件路径：{{confInfo.conf_file_path}})</b>

      <div class="row">
        <div class="col-lg-4">
          <div class="input-group">
            <input type="text" class="form-control highlight-kw" placeholder="高亮关键字" value="{{$route.query.kw}}">
            <span class="input-group-btn">
              <button class="btn btn-default" id="highlight-toggle" type="button" status="0"
                      v-on:click.stop.prevent="toggle_highlight($event)">高亮/取消</button>
            </span>
          </div><!-- /input-group -->
        </div><!-- /.col-lg-6 -->
      </div><!-- /.row -->

      <hr>
      <pre id="conf-detail" conf-id="{{$route.params.conf_id}}">{{confInfo.conf_content}}</pre>
    </div>
</template>
<script>

  import "jquery-highlight";
  import config from 'config';

  module.exports = {
    data: function(){
      return {
        confInfo: {}
      }
    },

    methods: {
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

    },

    ready: function () {
      var self = this;
      var conf_id = $('#conf-detail').attr('conf-id');
      $.ajax({
        url: config.baseUrl + '/conf_info/?conf_id=' + conf_id ,
        method: 'GET',
        success: function(data){
          self.confInfo = data.data;

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
