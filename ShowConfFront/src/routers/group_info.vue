<style scoped>
    /*@import '../styles/common.css';*/
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
        <h2 class="sub-header col-md-5">分组信息</h2>
        <span class="col-md-1 col-md-offset-6">
          <button class="btn btn-primary" v-on:click="back()">返回</button>
        </span>
      </div>
      <hr>

      <form>
        <div class="form-group row">
          <label for="name" class="col-sm-2 form-control-label">分组名称</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="name" v-model="groupInfo.name" placeholder="">
            <small class="text-muted">
              和机器IP任选一个
            </small>
          </div>
        </div>

        <div class="form-group row">
          <label for="conf_file_path" class="col-sm-2 form-control-label">配置文件路径<i class="text-muted">*</i></label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="conf_file_path" v-model="groupInfo.conf_file_path" placeholder="~/test_conf_show/test.erl">
          </div>
        </div>

        <div class="form-group row">
          <label for="comment" class="col-sm-2 form-control-label">备注信息</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="comment" v-model="groupInfo.comment" placeholder="">
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
        groupInfo:{
          id: 0,
          name: '',
          conf_file_path:'',
          comment: '',
        },
      }
    },

    methods: {
      back: function(){
        this.$router.go({name: 'groupList'});
      },
      onSubmit: function(){
        var self = this;

        var groupId = self.groupInfo.id;
        var method = 'POST';
        if (groupId > 0) method = "PUT";

        $.ajax({
          url: config.baseUrl + '/groups/' + groupId ,
          method: method,
          data: self.groupInfo,
          success: function(data){
            if (data.code < 0){
              alert(data.message);
            } else {
              self.$router.go({ name: 'groupList'});
            }

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
        _.merge(this.groupInfo, this.$route.query);
      }
    }


  }
</script>
