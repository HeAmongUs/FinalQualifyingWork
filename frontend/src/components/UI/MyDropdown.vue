<template>
  <div class="dropdown" @click="isOpen = !isOpen">
    <slot name="target"></slot>
    <div class="dropdown-content" :class="{ 'dropdown-open': isOpen }">
      <slot name="content"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "MyDropdown",
  data() {
    return {
      isOpen: false,
    }
  },
}
</script>

<style scoped lang="scss">
.dropdown {
  position: relative;
  transition: 0.3s;
  opacity: 1;
  border: 1px solid transparent;
  padding: 0 8px;
  svg {
    width: 4px;
  }
  &-content {
    opacity: 1;
    display: block;
    top: 0;
    left: -160px;
    position: absolute;
    width: 160px;
    height: 0;
  }
  &-open {
    height: auto;
  }
}
</style>
