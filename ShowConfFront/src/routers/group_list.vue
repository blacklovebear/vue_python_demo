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
      <h2 class="sub-header col-md-5">分组列表</h2>
      <span class="col-md-1 col-md-offset-6">
        <button class="btn btn-primary" v-on:click="add()">添加</button>
      </span>
    </div>
    <hr>
    <div class="row">
      <div class="col-md-4">
        <div class="form-inline form-group">
          <label>表格内搜索:</label>

          <div class="inner-addon right-addon display-one-line">
            <i class="glyphicon glyphicon-search"></i>
            <input v-model="searchQuery" type="text" class="form-control" placeholder="search" />
          </div>

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
  import Grid from '../components/grid';

  export default {
    components: {
      'yunba-grid': Grid
    },

    data() {
      return {
        // 表格过滤搜索
        searchQuery: '',

        gridColumns: ['name', 'is_leaf', 'conf_file_path', 'parent_name', 'comment', 'operate'],
        gridDisplayNames: {name: '分组名称', conf_file_path:'配置文件路径',
                          parent_name:"父节点名称", is_leaf: '是否为叶子分组',
                          comment: '备注信息', operate: '操作'},
        moreOperation:{
          operate: 'groupOperatePartial',
        },
        // 表格数据
        gridData: [],

      }
    },

    methods:{
      add() {
        this.$router.go({name: 'groupInfo'})
      },

      handleDeleteRow(groupId) {
        var self = this;
        var conclusion = confirm('确定删除?');
        if (!conclusion) {
          return
        }

        $.ajax({
          url: config.baseUrl + '/groups/' + groupId ,
          method: 'DELETE',
          success(data) {
            if (data.code < 0) alert(data.message);

            self.loadConfFileData();
          },
          error(error) {
            alert(JSON.stringify(error));
          }
        });

      },

      // 加载表格数据
      loadConfFileData() {
        var self = this;
        var url = config.baseUrl + '/groups';

        $.ajax({
          url: url,
          method: 'GET',
          success(data) {
            self.gridData = data.data;
          },
          error(error) {
            alert(JSON.stringify(error));
          }
        });
      }

    },

    ready() {
      this.loadConfFileData();
    }

  }
</script>
