<style scoped>
  @import '../styles/highlight.css';
  .conf-explain{
    margin-left: 50px;
  }
</style>
<template>
  <div>
    <h2 class="sub-header" style="display:inline-block">Configure Detail</h2>
    <span class="conf-explain">
      Host: {{confInfo.host_domain}}; File Path: {{confInfo.conf_file_path}}
    </span>

    <div class="row">
      <div class="col-md-4">
        <div class="input-group">
          <input type="text" class="form-control highlight-kw" placeholder="keyword" value="{{$route.query.kw}}">
          <span class="input-group-btn">
            <button class="btn btn-default" id="highlight-toggle" type="button" status="0"
                    v-on:click.stop.prevent="toggle_highlight($event)">Highlight toggle</button>
          </span>
        </div>
      </div>

      <div class="col-md-2 col-md-offset-5">
        <button class="btn btn-primary" type="button"
                v-on:click.stop.prevent="loadFileContent($route.params.conf_id)">Reload Configure</button>
      </div>

      <div class="col-md-1">
        <button class="btn btn-primary" type="button" v-on:click.stop.prevent="back()">Return</button>
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
  import "../jquery.link";

  export default {
    data() {
      return {
        confInfo: {},
        fileLoadResult:{},
      }
    },

    methods: {
      back() {
        this.$router.go({name: 'index'});
      },

      toggle_highlight(event) {
        let value = $('.highlight-kw').val();
        let status = $(event.toElement).attr('status');
        let confDetailEle = $('#conf-detail');

        if (status === '0') {
          confDetailEle.highlight(value);
          $(event.toElement).attr('status', '1');
        } else {
          confDetailEle.unhighlight(value);
          $(event.toElement).attr('status', '0');
        }
      },

      // 将文件内容从机器上加载到数据库
      loadFileContent(conf_id) {
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

    ready() {
      let self = this;
      let confDetailEle = $('#conf-detail');

      let conf_id = confDetailEle.attr('conf-id');
      $.ajax({
        url: config.baseUrl + '/confs/' + conf_id ,
        method: 'GET',
        success(data) {
          self.confInfo = data.data;
          self.fileLoadResult = data.load_result;

          setTimeout(function(){
            // 为内容中的yunba.io的机器Add链接, 第二个参数为link的 href
            confDetailEle.link('a\\w+-[\\w]+-[\\w]+', "#!/?no_cache=1&kw=");

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
