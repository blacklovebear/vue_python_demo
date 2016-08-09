<style scoped>
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
        <h2 class="sub-header col-md-5">Group Info</h2>
        <span class="col-md-1 col-md-offset-6">
          <button class="btn btn-primary" v-on:click="back()">Return</button>
        </span>
      </div>
      <hr>

      <form>
        <div class="form-group row">
          <label for="name" class="col-sm-2 form-control-label">Group Name</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="name" v-model="groupInfo.name" placeholder="">
            <small class="text-muted">
              Alternative with IP
            </small>
          </div>
        </div>

        <div class="form-group row">
          <label for="name" class="col-sm-2 form-control-label">Is Leaf</label>
          <div class="col-sm-6">
            <label class="form-check-inline">
              <input class="form-check-input" type="radio" name="is_leaf" value="true" v-model="groupInfo.is_leaf"> Yes
            </label>
            <label class="form-check-inline">
              <input class="form-check-input" type="radio" name="is_leaf" value="false" v-model="groupInfo.is_leaf"> No
            </label>
          </div>
        </div>

        <div class="form-group row" v-show="groupInfo.is_leaf ==='true'">
          <label for="conf_file_path" class="col-sm-2 form-control-label">Configure Path<i class="text-muted">*</i></label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="conf_file_path" v-model="groupInfo.conf_file_path" placeholder="~/test_conf_show/test.erl">
          </div>
        </div>

        <div class="form-group row">
          <label for="comment" class="col-sm-2 form-control-label">Comment</label>
          <div class="col-sm-6">
            <input type="text" class="form-control" id="comment" v-model="groupInfo.comment" placeholder="">
          </div>
        </div>

        <div class="form-group row">
          <label for="comment" class="col-sm-2 form-control-label">Parent</label>
          <div class="col-sm-6">
              <group-section :parent-section.sync="groupInfo.parent"
              :search-text="groupInfo.parent_name"></group-section>
          </div>
        </div>

        <div class="form-group row">
          <div class="col-sm-offset-2 col-sm-6">
            <button type="button" class="btn btn-primary" v-on:click.prevent="onSubmit()">Submit</button>
          </div>
        </div>
      </form>

    </div>
</template>

<script>
  import config from 'config';
  import GroupSection from '../components/groupSection';

  export default {
    components: {
      'group-section': GroupSection
    },

    data() {
      return {
        groupInfo:{
          id: 0,
          name: '',
          is_leaf:'true',
          conf_file_path:'',
          parent: 0,
          parent_name: 'select group',
          comment: '',
        },
      }
    },

    methods: {
      back() {
        this.$router.go({name: 'groupList'});
      },

      onSubmit() {
        let self = this;
        let groupId = self.groupInfo.id;
        let method = groupId > 0 ? 'PUT' : 'POST';

        $.ajax({
          url: config.baseUrl + '/groups/' + groupId,
          method: method,
          data: self.groupInfo,
          success(data) {
            if (data.code < 0){
              alert(data.message);
            } else {
              self.$router.go({name: 'groupList'});
            }
          },
          error(error) {
            alert(JSON.stringify(error));
          }
        });
      }
    },

    ready() {
      // 表示Edit，会传当前记录的信息过来
      if (this.$route.query){
        _.merge(this.groupInfo, this.$route.query);
      }
    }

  }
</script>
