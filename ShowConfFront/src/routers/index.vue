<style scoped>
  @import '../styles/formInput.css';

  .row h2 {
    line-height: 0px;
  }

</style>
<template>
    <div>
      <!-- Example row of columns -->
      <div class="row" style="margin-top:15px">
        <h2 class="sub-header col-xs-5">配置文件列表</h2>
        <span class="col-xs-1 col-xs-offset-6">
          <button class="btn btn-primary" v-on:click="add()">添加</button>
        </span>
      </div>
      <hr>
      <div class="row">
          <div class="col-xs-4">
              <div class="form-inline form-group">
                <label class="control-label">表格:</label>

                <div class="inner-addon right-addon display-one-line">
                  <i class="glyphicon glyphicon-search"></i>
                  <input v-model="searchQuery" type="text" class="form-control" placeholder="search" value="{{$route.query.kw}}"/>
                </div>

              </div>
          </div>
          <div class="col-xs-4">
            <group-search :group.sync="group" v-on:group-change="handleGroupChange" :search-text="groupText"></group-search>
          </div>

          <div class="col-xs-4">
              <div class="form-inline form-group" style="text-align:right">
                <label class="control-label">文件内容:</label>
                <div class="inner-addon right-addon display-one-line">
                  <i class="glyphicon glyphicon-search"></i>
                  <input v-model="keyWord" type="text" class="form-control" placeholder="search" />
                </div>
                <button class="btn btn-primary" v-on:click="searchKeyWord()">Go</button>
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
        groupText: '请选择一个分组',

        gridColumns: ['host_domain',
                      'conf_file_path', 'group_name', 'last_ch_time', 'id', 'operate'],
        gridDisplayNames: { host_domain: "所在服务器",
                            conf_file_path: '配置文件路径',
                            group_name: '所属分组名',
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

      handleGroupChange: function(item){
        // 虽然函数有传值出来，还是使用双向绑定的值
        localStorage.setItem('index_group', item.id);
        localStorage.setItem('index_group_name', item.name);
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
      // 表示group不采用缓存
      if (this.$route.query.no_cache){
        // do nothing
      } else {
        this.group = localStorage.getItem('index_group') || 0;
        this.groupText = localStorage.getItem('index_group_name') || '请选择一个分组';
      }

      this.loadConfFileData();
    }

  }
</script>
