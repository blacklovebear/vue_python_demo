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
      <h2 class="sub-header col-xs-5">Configure List</h2>
      <span class="col-xs-1 col-xs-offset-6">
        <button class="btn btn-primary" v-on:click="add()">Add</button>
      </span>
    </div>
    <hr>
    <div class="row">
        <div class="col-xs-3">
            <div class="form-inline form-group">
              <div class="inner-addon right-addon display-one-line">
                <i class="glyphicon glyphicon-search"></i>
                <input v-model="searchQuery" type="text" class="form-control" placeholder="search" value="{{$route.query.kw}}"/>
              </div>

            </div>
        </div>
        <div class="col-xs-4">
          <group-search :group.sync="group" v-on:group-change="handleGroupChange" :search-text="groupText"></group-search>
        </div>

        <div class="col-xs-5">
            <div class="form-inline form-group" style="text-align:right">
              <label class="control-label">File Content:</label>
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
  import Grid from '../components/grid';
  import GroupSearch from '../components/groupSearch';

  export default {
    components: {
      'yunba-grid': Grid,
      'group-search': GroupSearch
    },

    data() {
      return {
        // 表格过滤搜索
        searchQuery: '',
        keyWord:'',
        group: 0,
        groupText: 'Select group',
        gridColumns: ['host_domain', 'conf_file_path', 'group_name', 'last_ch_time', 'id', 'operate'],
        gridDisplayNames: { host_domain: "Host Domain",
                            conf_file_path: 'File Path',
                            group_name: 'Group',
                            last_ch_time: 'Last Sync',
                            id: 'See',
                            operate: 'Operation',
                          },
        moreOperation:{
          id: "listInfoPartial",
          operate: 'listOperatePartial'
        },
        // 表格数据
        gridData: [],
      }
    },

    methods:{
      add() {
        this.$router.go({ name: 'confInfo'});
      },

      // 通过关键词搜索
      searchKeyWord(kw, group) {
        this.loadConfFileData();
      },

      handleGroupChange(item) {
        // 虽然函数有传值出来，还是使用双向绑定的值
        localStorage.setItem('index_group', item.id);
        localStorage.setItem('index_group_name', item.name);
        this.loadConfFileData();
      },

      handleDeleteRow(confId) {
        let self = this;
        let conclusion = confirm('确定删除?');
        if (!conclusion) {
          return
        }

        $.ajax({
          url: config.baseUrl + '/confs/' + confId ,
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
        let self = this;
        let url = config.baseUrl + '/confs';

        $.ajax({
          url: url,
          method: 'GET',
          data: { kw: $.trim(self.keyWord), group_id: self.group },
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
      // 表示group不采用缓存
      if (this.$route.query.no_cache){
        // do nothing
      } else {
        this.group = localStorage.getItem('index_group') || 0;
        this.groupText = localStorage.getItem('index_group_name') || 'Select group';
      }

      this.loadConfFileData();
    }

  }
</script>
