<template>
  <div class="row login-box valign-wrapper">
    <div class="col s12 m8 offset-m2 l4 offset-l4">
      <div class="row scale-transition" v-bind:class="{'scale-out': !errorMessage}">
        <div class="card-panel deep-orange accent-2">
          <span class="white-text">{{errorMessage}}</span>
        </div>
      </div>
      <div class="row">
        <div class="card">
          <div class="card-content">
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

      isLoad: false,
      errorMessage: ""
    };
  },
  computed: {
    // isSessionValid: () => 'Any Text',
    ...mapGetters(["session/isValid"])
  },
  methods: {
    ...mapActions({ RetriveToken: "session/RetriveToken" }),
    submit: async function() {
      this.isLoad = true;
      await this.RetriveToken({
        login: this.login,
        password: this.password
      })
        .then(result => this.$router.push({ name: "Master" }))
        .catch(error => {
          (this.login = ""), (this.password = ""), (this.errorMessage = error);
        });

      this.isLoad = false;
    }
  }
};
</script>

<style>
.login-box {
  height: 100vh;
}
</style>