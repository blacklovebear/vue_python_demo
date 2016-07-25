<style scoped>
    /*@import '../styles/common.css';*/
    .form-control-label {
      text-align: right;
    }
    .text-muted {
      color:#d9534f;
    }
</style>
<template>
    <div>
      <!-- Example row of columns -->
      <h2 class="sub-header">文件信息录入</h2>
        <div class="alert"
          v-show="typeof status.code !== 'undefined' "
          v-bind:class="{'alert-success':status.code === 0, 'alert-danger':status.code < 0}">
          <button type="button" class="close" data-dismiss="alert">×</button>
          <strong>{{status.message}}</strong>
        </div>
      <hr>

      <form>
        <div class="form-group row">
          <label for="host_domain" class="col-sm-2 form-control-label">所在机器域名</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="host_domain" v-model="fileInfo.host_domain" placeholder="eg:abj-elogic-test1.yunba.io">
            <small class="text-muted">
              和机器IP任选一个
            </small>
          </div>
        </div>

        <div class="form-group row">
          <label for="host_ip" class="col-sm-2 form-control-label">所在机器IP</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="host_ip" v-model="fileInfo.host_ip" placeholder="127.0.0.1">
          </div>
        </div>

        <div class="form-group row">
          <label for="host_user_name" class="col-sm-2 form-control-label">机器用户名<i class="text-muted">*</i></label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="host_user_name" v-model="fileInfo.host_user_name" placeholder="yunba">
          </div>
        </div>

        <div class="form-group row">
          <label for="ssh_key_path" class="col-sm-2 form-control-label">SSH key所在路径</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="ssh_key_path" v-model="fileInfo.ssh_key_path" placeholder="/Users/weizhiyun078/.ssh/id_rsa">
            <small class="text-muted">
              和用户密码任填一个
            </small>
          </div>
        </div>

        <div class="form-group row">
          <label for="host_pass" class="col-sm-2 form-control-label">用户密码</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="host_pass" v-model="fileInfo.host_pass" placeholder="密码">
          </div>
        </div>

        <div class="form-group row">
          <label for="conf_file_path" class="col-sm-2 form-control-label">配置文件路径<i class="text-muted">*</i></label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="conf_file_path" v-model="fileInfo.conf_file_path" placeholder="~/test_conf_show/test.erl">
          </div>
        </div>

        <div class="form-group row">
          <label for="service_name" class="col-sm-2 form-control-label">所属服务名称</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="service_name" v-model="fileInfo.service_name" placeholder="服务名">
          </div>
        </div>

        <div class="form-group row">
          <label for="comment" class="col-sm-2 form-control-label">备注信息</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="comment" v-model="fileInfo.comment" placeholder="备注">
          </div>
        </div>

        <div class="form-group row">
          <label for="group" class="col-sm-2 form-control-label">分组</label>
          <div class="col-sm-6">
            <yunba-group :group.sync="fileInfo.group_id"></yunba-group>
          </div>
        </div>


        <div class="form-group row">
          <div class="col-sm-offset-2 col-sm-6">
            <button type="button" class="btn btn-primary" v-on:click.prevent="onSubmit()">提交</button>
          </div>
        </div>
      </form>

    </div>


</template>
<script>
  import config from 'config';
  module.exports = {
    data: function(){
      return {
        fileInfo:{
          host_domain: '',
          host_ip: '',
          host_user_name: '',
          ssh_key_path: '',
          host_pass: '',
          conf_file_path: '',
          service_name: '',
          comment: '',
          group_id: 0,
        },
        // 最终返回状态
        status:{},
      }
    },

    methods: {
      onSubmit: function(){
        var self = this;
        _.forIn(self.fileInfo, function(value, key){
          if (key !== 'group_id'){
            self.fileInfo[key] = _.trim(value)
          }
        });

        $.ajax({
          url: config.baseUrl + '/input/file_info/' ,
          method: 'POST',
          data: self.fileInfo,
          success: function(data){
            self.status.code = data.code;
            self.status.message = data.message;

            if (data.code < 0){
              alert(data.message);
            }

            self.$router.go({ name: 'index'});

          },
          error: function(error){
            alert(JSON.stringify(error));
          }
        });


      }
    },

    ready: function () {
      // 表示修改，会传当前记录的信息过来
      if (this.$route.query){
        _.merge(this.fileInfo, this.$route.query);
      }
    }


  }
</script>
