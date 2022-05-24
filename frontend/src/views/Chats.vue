<template>
  <div class="chats">
    <messenger />
  </div>
</template>

<script>
import Messenger from "../components/chats/Messenger"
export default {
  name: "Chats",
  components: { Messenger },
}
</script>

<style scoped></style>
