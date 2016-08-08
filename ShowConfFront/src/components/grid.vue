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

  /*分页*/
  .pagination {
    margin: 0px;
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
          entry in pageData
          | filterBy filterKey
          | orderBy sortKey sortOrders[sortKey]">
          <td v-for="key in columns">
            <span v-if="typeof moreOperation[key] !== 'undefined'">
              <partial :name="moreOperation[key]"></partial>
            </span>
            <span v-else>{{entry[key]}}</span>

          </td>
        </tr>
      </tbody>
    </table>
    <nav>
      <ul class="pagination pagination-sm">
        <li class="page-item">
          <a class="page-link" v-on:click.stop.prevent='prePage()' aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">Previous</span>
          </a>
        </li>
        <li class="page-item" v-for="index in total">
          <a class="page-link" v-on:click.stop.prevent="gotoPage(index + 1)">{{index + 1}}</a>
        </li>

        <li class="page-item">
          <a class="page-link" v-on:click.stop.prevent="nextPage()" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">Next</span>
          </a>
        </li>
      </ul>
    </nav>

</template>

<script>
  import config from 'config';
  import Vue from 'vue';

  export default {
    // 表格的一些特殊操作
    partials: {
      'listInfoPartial': "<a v-link=\"{name: 'conf_detail', params: {conf_id: entry[key]}, query:{kw: keyWord}}\">详情</a>| \
              <a v-link=\"{name: 'jsonview', params: {conf_id: entry[key]}, query:{kw: keyWord}}\">JSON</a>",

      'listOperatePartial': "<a v-link=\"{name: 'confInfo', query:entry }\">修改</a>",

      'groupOperatePartial': "<a v-link=\"{name: 'groupInfo', query:entry }\">修改</a>"
    },

    replace: true,

    props: {
      gridData: Array,
      columns: Array,
      filterKey: String,
      displayNames:Object,
      moreOperation: Object,
      // 文件内容搜索关键字，只为给详情链接使用
      keyWord:String
    },

    data() {
      let sortOrders = {}
      this.columns.forEach(function (key) {
        sortOrders[key] = 1
      })
      return {
        sortKey: '',
        sortOrders: sortOrders,
        // 每页的行数
        perPage: 15,
        currentPage: 1,
      }
    },

    computed: {
      filteredData() {
        const filter = Vue.filter('filterBy')
        return filter(this.gridData, this.filterKey)
      },

      pageData() {
        let start = (this.currentPage - 1) * this.perPage;
        let end = this.currentPage * this.perPage;
        let realEnd = end > this.filteredData.length ? this.filteredData.length : end;

        return _.slice(this.filteredData, start, realEnd);
      },
      // 总页数
      total() {
        // 如果总页数发生改变，比较将当前选中的页数初始化为1
        this.currentPage = 1;
        return _.ceil(this.filteredData.length * 1.0 / this.perPage);
      },
    },

    methods: {
      sortBy(key) {
        this.sortKey = key
        this.sortOrders[key] = this.sortOrders[key] * -1
      },

      // 删除一行数据
      deleteRow(id) {
        this.$dispatch('delete-row', id);
      },

      nextPage() {
        let current = this.currentPage;
        let total = this.total;
        this.currentPage =  current + 1 > total ? total : current + 1;
      },

      gotoPage(page) {
        let total = this.total;
        this.currentPage =  page > total || page < 1 ? 1 : page;
      },

      prePage() {
        let current = this.currentPage;
        let total = this.total;
        this.currentPage =  current - 1 < 1 ? 1 : current - 1;
      }

    },
  }
</script>
