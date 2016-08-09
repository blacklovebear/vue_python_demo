<style scoped>
  .form-control-label {
    text-align: right;
  }
  .text-muted {
    color:#d9534f;
  }
  .row h2 {
    line-height: 0px;
  }
</style>

<template>
  <div>
    <div class="row" style="margin-top:15px">
      <h2 class="sub-header col-md-5">Configure Info</h2>
      <span class="col-md-1 col-md-offset-6">
        <button class="btn btn-primary" v-on:click="back()">Return</button>
      </span>
    </div>

    <hr>

    <form>
      <div class="form-group row">
        <label for="host_domain" class="col-sm-2 form-control-label">Host Domain</label>
        <div class="col-sm-6">
          <input type="text" class="form-control" id="host_domain" v-model="fileInfo.host_domain" placeholder="eg:abj-elogic-test1.yunba.io">
          <small class="text-muted">
            Alternative with IP
          </small>
        </div>
      </div>

      <div class="form-group row">
        <label for="host_ip" class="col-sm-2 form-control-label">IP</label>
        <div class="col-sm-6">
          <input type="text" class="form-control" id="host_ip" v-model="fileInfo.host_ip" placeholder="127.0.0.1">
        </div>
      </div>

      <div class="form-group row">
        <label for="host_user_name" class="col-sm-2 form-control-label">User name<i class="text-muted">*</i></label>
        <div class="col-sm-6">
          <input type="text" class="form-control" id="host_user_name" v-model="fileInfo.host_user_name" placeholder="yunba">
        </div>
      </div>

      <div class="form-group row">
        <label for="ssh_key_path" class="col-sm-2 form-control-label">SSH Key Path</label>
        <div class="col-sm-6">
          <input type="text" class="form-control" id="ssh_key_path" v-model="fileInfo.ssh_key_path" placeholder="/Users/weizhiyun078/.ssh/id_rsa">
          <small class="text-muted">
            Alternative with Password
          </small>
        </div>
      </div>

      <div class="form-group row">
        <label for="host_pass" class="col-sm-2 form-control-label">Password</label>
        <div class="col-sm-6">
          <input type="password" class="form-control" id="host_pass" v-model="fileInfo.host_pass" placeholder="password">
        </div>
      </div>

      <div class="form-group row">
        <label for="comment" class="col-sm-2 form-control-label">Comment</label>
        <div class="col-sm-6">
          <input type="text" class="form-control" id="comment" v-model="fileInfo.comment" placeholder="">
        </div>
      </div>

      <div class="form-group row">
        <label for="group" class="col-sm-2 form-control-label">Group</label>
        <div class="col-sm-6">
          <group-search :group.sync="fileInfo.group_id" :search-text="fileInfo.group_name"></group-search>
        </div>
      </div>


      <div class="form-group row">
        <div class="col-sm-offset-2 col-sm-6">
          <button type="button" class="btn btn-primary" v-on:click.prevent="onSubmit()">Submit</button>
        </div>
      </div>
    </form>

  </div>
</template>

<script>
  import config from 'config';
  import GroupSearch from '../components/groupSearch';

  export default {
    components: {
      'group-search': GroupSearch
    },

    data() {
      return {
        fileInfo:{
          id: 0,
          host_domain: '',
          host_ip: '',
          host_user_name: '',
          ssh_key_path: '',
          host_pass: '',
          conf_file_path: '',
          comment: '',
          group_id: 0,
          group_name: ''
        },
        // 最终Return状态
        status:{},
      }
    },

    methods: {
      back() {
        this.$router.go({name: 'index'});
      },

      onSubmit() {
        let self = this;
        let confId = self.fileInfo.id;
        let method =  confId > 0 ? 'PUT' : 'POST';

        $.ajax({
          url: config.baseUrl + '/confs/' + confId ,
          method: method,
          data: self.fileInfo,
          success(data) {
            self.status.code = data.code;
            self.status.message = data.message;

            if (data.code < 0){
              alert(data.message);
            } else {
              self.$router.go({ name: 'index'});
            }
          },
          error(error) {
            alert(JSON.stringify(error));
          }
        });

      }
    },

    ready() {
      // 表示Edit，会传当前记录的信息过来
      if (this.$route.query){
        _.merge(this.fileInfo, this.$route.query);
      }
    }

  }
</script>
