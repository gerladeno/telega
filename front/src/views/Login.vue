<template>
  <div class="row login-box valign-wrapper">
    <div class="col s12 m8 offset-m2 l4 offset-l4">
      <div class="row">
        <div class="card">
          <div class="card-content">
            {{isSessionValid}}
            <form @submit.prevent="submit()">
              <div class="input-field">
                <input placeholder="Login" id="login" type="text" class="validate" v-model="login" />
                <label class="active" for="login">Login</label>
              </div>
              <div class="input-field">
                <input
                  placeholder="Password"
                  id="password"
                  type="password"
                  class="validate"
                  v-model="password"
                />
                <label class="active" for="password">{{login}}</label>
              </div>
              <div class="right-align">
                <button type="submit" class="btn waves-effect">Login</button>
              </div>
            </form>
          </div>
          <div v-if="isLoad" class="progress">
            <div class="indeterminate"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import { mapGetters } from "vuex";
export default {
  name: "login",
  data() {
    return {
      login: "",
      password: "",

      isLoad: false
    };
  },
  computed: {
    ...mapGetters(["isSessionValid"])
  },
  methods: {
    ...mapActions(["RetriveToken"]),
    submit: function() {
      this.isLoad = true;
      this.RetriveToken({ login: this.login, password: this.password });
    }
  }
};
</script>

<style>
.login-box {
  height: 100vh;
}
</style>