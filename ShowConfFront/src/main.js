/**
 * Created by aresn on 16/6/20.
 */
import Vue from 'vue';
import VueRouter from 'vue-router';
import App from 'components/app.vue';
import Grid from 'components/grid.vue';
import Group from 'components/group.vue';


// use bootstrap
import 'bootstrap-webpack';


// register
Vue.component('yunba-grid', Vue.extend(Grid));
Vue.component('yunba-group', Vue.extend(Group));

// 注册表格中使用的自定义指令
Vue.partial('listOptionPartial', "<a v-link=\"{name: 'detail', params: {conf_id: entry[key]}, query:{kw: keyWord}}\">详情</a>| \
              <a v-link=\"{name: 'jsonview', params: {conf_id: entry[key]}, query:{kw: keyWord}}\">Json</a>");

Vue.partial('loadConfPartial', "<a v-on:click.stop.prevent='loadFileContent(entry.id)'>重新加载</a>");
Vue.partial('operatePartial', "<a v-link=\"{name: 'inputFile', query:entry }\">修改</a>");



Vue.use(VueRouter);

// 开启debug模式
Vue.config.debug = true;

// 路由配置
var router = new VueRouter({
    // 是否开启HTML5的history模式,开启后,需服务端支持,否则404
    history: false
});

router.map({
    '/index': {
      name: 'index',
      component: function (resolve) {
        require(['./routers/index.vue'], resolve);
      }
    },
    '/detail/:conf_id/': {
      name: 'detail',
      component: function (resolve) {
        require(['./routers/detail.vue'], resolve);
      }
    },
    '/jsonview/:conf_id': {
      name: 'jsonview',
      component: function (resolve) {
        require(['./routers/json_view.vue'], resolve);
      }
    },
    '/input/file': {
      name: 'inputFile',
      component: function (resolve) {
        require(['./routers/input_file_info.vue'], resolve);
      }
    }
});

router.beforeEach(function () {
    window.scrollTo(0, 0);
});

router.afterEach(function (transition) {

});

router.redirect({
    '*': "/index"
});
router.start(App, '#app');