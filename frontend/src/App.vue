<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script>
import EmptyLayout from "@/layouts/EmptyLayout"
import MainLayout from "@/layouts/MainLayout"

export default {
  components: {
    MainLayout,
    EmptyLayout,
  },
  computed: {
    layout() {
      return (this.$route.meta.layout || "empty") + "-layout"
    },
  },
}
</script>

<style lang="scss">
@import "~materialize-css/dist/css/materialize.min.css";
@import "assets/messenger.colors";
#app {
  text-align: center;
  background: $app-bg;
  height: 100vh;
}
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}
.flex {
  display: flex;
}
.flex-justify-start {
  justify-content: flex-start;
  align-items: center;
}
.flex-align-end {
  justify-content: center;
  align-items: end;
}
.flex-center {
  justify-content: center;
  align-items: center;
}
.absolute {
  position: absolute;
}
.icon-prefix {
  top: 15px;
  left: 5px;
}
.icon-prefix + input,
.icon-prefix + input + label {
  padding-left: 25px !important;
  width: calc(100% - 25px) !important;
}
.helper-text.invalid {
  color: #f44336;
}
textarea {
  resize: none;

  &:focus {
    outline: none;
    cursor: text;
  }
}
</style>
