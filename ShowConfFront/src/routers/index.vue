<style scoped>
    /*@import '../styles/common.css';*/
    .row h2 {
      line-height: 0px;
    }
</style>
<template>
    <div>
      <!-- Example row of columns -->
      <div class="row" style="margin-top:15px">
        <h2 class="sub-header col-md-5">配置文件列表</h2>
        <span class="col-md-1 col-md-offset-6">
          <button class="btn btn-primary" v-on:click="add()">添加</button>
        </span>
      </div>
      <hr>
      <div class="row">
          <div class="col-md-5">
              <div class="form-inline form-group">
                  <label>文件内容搜索:</label>
                  <input v-model="keyWord" class="form-control">
                  <button class="btn btn-primary" v-on:click="searchKeyWord()">Go</button>
              </div>
          </div>
          <div class="col-md-3">
            <yunba-group :group.sync="group" v-on:group-change="handleGroupChange"></yunba-group>
          </div>

          <div class="col-md-4">
              <div class="form-inline form-group" style="text-align:right">
                  <label>表格内搜索:</label>
                  <input v-model="searchQuery" class="form-control">
              </div>
          </div>

      </div>
      <div class="table-responsive">
        <div class="vuetable-wrapper">
           <yunba-grid
            :grid-data="gridData"
            :columns="gridColumns"
            :display-names="gridDisplayNames"
            :more-operation="moreOperation"
            :filter-key="searchQuery"
            :key-word="keyWord"
            v-on:delete-row="handleDeleteRow"
            >
          </yunba-grid>
        </div>

      </div>
      <hr>

    </div>


</template>
<script>
  import config from 'config';
  module.exports = {
    data: function(){
      return {
        // 表格过滤搜索
        searchQuery: '',
        keyWord:'',
        group: 0,

        gridColumns: ['host_domain',
                      'conf_file_path', 'last_ch_time', 'id', 'operate'],
        gridDisplayNames: { host_domain: "所在服务器",
                            conf_file_path: '配置文件路径',
                            last_ch_time: '最近同步时间',
                            id: '查看',
                            operate: '操作',
                          },
        moreOperation:{
          id: "listOptionPartial",
          operate: 'operatePartial'
        },
        // 表格数据
        gridData: [],


      }
    },

    methods:{
      add: function(){
        this.$router.go({ name: 'confInfo'});
      },

      // 通过关键词搜索
      searchKeyWord:function(kw, group){
        this.loadConfFileData();
      },

      handleGroupChange: function(group){
        // 虽然函数有传值出来，还是使用双向绑定的值
        this.loadConfFileData();
      },

      handleDeleteRow: function(confId){
        var self = this;
        var conclusion = confirm('确定删除?');
        if (!conclusion) {
          return
        }

        $.ajax({
          url: config.baseUrl + '/confs/' + confId ,
          method: 'DELETE',
          success: function(data){
            if (data.code < 0) alert(data.message);

            self.loadConfFileData();
          },
          error: function(error){
            alert(JSON.stringify(error));
          }
        });

      },

      // 加载表格数据
      loadConfFileData:function(){
        var self = this;
        var url = config.baseUrl + '/confs';

        $.ajax({
          url: url,
          method: 'GET',
          data: { kw: $.trim(self.keyWord), group_id: self.group },
          success: function(data){
            self.gridData = data.data;
          },
          error: function(error){
            alert(JSON.stringify(error));
          }
        });
      }

    },

    ready: function () {
      this.loadConfFileData();
    }

  }
</script>
