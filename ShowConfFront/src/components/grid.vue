<style scoped>
  .vuetable th.sortable:hover {
      color: #2185d0;
      cursor: pointer;
  }

  /* Loading Animation: */
  .vuetable-wrapper {
      opacity: 1;
      position: relative;
      filter: alpha(opacity=100); /* IE8 and earlier */
  }


  /*表格头部样式*/
  th.active .arrow {
    opacity: 1;
  }

  .arrow {
    display: inline-block;
    vertical-align: middle;
    width: 0;
    height: 0;
    margin-left: 5px;
    opacity: 0.66;
  }

  .arrow.asc {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 4px solid #000;
  }

  .arrow.dsc {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid #000;
  }
</style>
<template>

    <table class="vuetable table table-bordered table-striped table-hover">
      <thead>
        <tr>
          <th v-for="key in columns"
            @click="sortBy(key)"
            :class="{active: sortKey == key}">
            <!-- {{key | capitalize}} -->
            {{ displayNames[key] }}
            <span class="arrow"
              :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="
          entry in data
          | filterBy filterKey
          | orderBy sortKey sortOrders[sortKey]">
          <td v-for="key in columns">
            <!-- id跳转到详细 -->
            <!-- <span v-if="key === 'id'">
              <a v-link="{name: 'detail', params: {conf_id: entry[key]}}">详情</a>|
              <a v-link="{name: 'jsonview', params: {conf_id: entry[key]}}">Json</a>
            </span>
            <span v-else>{{entry[key]}}</span> -->
            <span v-if="typeof moreOperation[key] !== 'undefined'">
              <partial :name="moreOperation[key]"></partial>
            </span>
            <span v-else>{{entry[key]}}</span>

          </td>
        </tr>
      </tbody>
    </table>

</template>
<script>
  import config from 'config';
  module.exports = {
    replace: true,
    props: {
      data: Array,
      columns: Array,
      filterKey: String,
      displayNames:Object,
      moreOperation: Object,
      // 文件内容搜索关键字，只为给详情链接使用
      keyWord:String
    },
    data: function () {
      var sortOrders = {}
      this.columns.forEach(function (key) {
        sortOrders[key] = 1
      })
      return {
        sortKey: '',
        sortOrders: sortOrders
      }
    },
    methods: {
      sortBy: function (key) {
        this.sortKey = key
        this.sortOrders[key] = this.sortOrders[key] * -1
      },

      // 将文件内容从机器上加载到数据库
      loadFileContent: function(conf_id){
        $.ajax({
          url: config.baseUrl + '/load_conf/?conf_id=' + conf_id ,
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
    }
  }
</script>
