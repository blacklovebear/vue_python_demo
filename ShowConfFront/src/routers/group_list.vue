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
      <h2 class="sub-header col-md-5">Group List</h2>
      <span class="col-md-1 col-md-offset-6">
        <button class="btn btn-primary" v-on:click="add()">Add</button>
      </span>
    </div>
    <hr>
    <div class="row">
      <div class="col-md-4">
        <div class="form-inline form-group">
          <div class="inner-addon right-addon display-one-line">
            <i class="glyphicon glyphicon-search"></i>
            <input v-model="searchQuery" type="text" class="form-control" placeholder="search" />
          </div>

        </div>
      </div>
      <div class="col-md-2">
        <select class="form-control" v-model="isLeaf" v-on:change="loadConfFileData()">
          <option value="0">All</option>
          <option value="1">Only Leaf</option>
          <option value="2">Not Leaf</option>
        </select>
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
        gridDisplayNames: {name: 'Group Name', conf_file_path:'Configure Path',
                           parent_name:"Parent Name", is_leaf: 'Is Leaf',
                           comment: 'Comment', operate: 'Operation'
                          },
        moreOperation: {
          operate: 'groupOperatePartial',
        },
        // 表格数据
        gridData: [],

        isLeaf: 0,

      }
    },

    methods:{
      add() {
        this.$router.go({name: 'groupInfo'})
      },

      handleDeleteRow(groupId) {
        let self = this;
        let conclusion = confirm('Are you sure?');
        if (!conclusion) {
          return
        }

        $.ajax({
          url: config.baseUrl + '/groups/' + groupId ,
          method: 'DELETE',
          success(data) {
            if (data.code < 0)
              alert(data.message);

            self.loadConfFileData();
          },
          error(error) {
            alert(JSON.stringify(error));
          }
        });
      },

      // 加载表格数据
      loadConfFileData() {
        let self = this;
        let url = config.baseUrl + '/groups';

        $.ajax({
          url: url,
          method: 'GET',
          data:{is_leaf: self.isLeaf},
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
