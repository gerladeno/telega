<template>
  <div class="row login-box valign-wrapper">
    <div class="col s12 m8 offset-m2 l4 offset-l4">
      <div class="row">
        <div class="card">
          <div class="card-content">
            <form>
              <div class="input-field">
                <input placeholder="Login" id="login" type="text" class="validate" />
                <label class="active" for="login">Login</label>
              </div>
              <div class="input-field">
                <input placeholder="Password" id="password" type="password" class="validate" />
                <label class="active" for="password">Password</label>
              </div>
              <div class="right-align">
                <button type="submit" class="btn waves-effect">Login</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- <div class="valign-wrapper row login-box">
    <div class="col card s10 pull-s1 m6 pull-m3 l4 pull-l4">
      <form>
        <div class="card-content">
          <span class="card-title"></span>
          <div class="row">
            <div class="input-field col s12">
              <label for="email">Login</label>
              <input type="email" class="validate" name="Login" id="login" />
            </div>
            <div class="input-field col s12">
              <label for="password">Pass</label>
              <input type="password" class="validate" name="password" id="password" />
            </div>
          </div>
        </div>
        <div class="card-action right-align">
          <button type="reset" id="reset" class="btn-flat grey-text">Reset</button>
          <button type="submit" class="btn blue-grey " value="Login">Login</button>
        </div>
      </form>
    </div>
  </div>-->
</template>

<script>
export default {
  // methods: {
  //   reset: function() {
  //     $("label").removeClass("active");
  //   }
  // }
};
</script>

<style>
.login-box {
  height: 100vh;
}
</style>