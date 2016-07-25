<style scoped>
</style>
<template>

    <select class="form-control" v-model="group" v-on:change="onChange()">
      <option :value="0">请选择分组</option>

      <option v-for="item in groupList" :value="item.id">
        {{item.name}}
      </option>
    </select>

</template>
<script>
  import config from 'config';
  module.exports = {
    props: ['group'],

    data: function () {
      return {
        groupList:[],
      }
    },

    methods: {
      onChange: function(){
        this.$dispatch('group-change', this.group);
      },

      loadGroupList: function(){
        var self = this;
        $.ajax({
          url: config.baseUrl + '/groups',
          method: 'GET',
          success: function(data){
            self.groupList = data.data;
          },
          error: function(error){
            alert(JSON.stringify(error));
          }
        });
      },

    },

    ready: function(){
      this.loadGroupList();
    }
  }
</script>
