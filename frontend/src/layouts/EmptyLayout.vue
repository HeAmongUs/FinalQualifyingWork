<template>
  <div class="empty-layout">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "EmptyLayout",
}
</script>

<style scoped>
.empty-layout {
  background: #ddd;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  min-height: 500px;
}
</style>
