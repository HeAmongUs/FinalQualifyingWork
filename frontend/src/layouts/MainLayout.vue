<template>
  <div class="app-main-layout">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "MainLayout",
  components: {},
  data() {
    return {}
  },
  mounted() {
    this.$store.dispatch("getCurrentUser")
  },
}
</script>

<style scoped></style>
