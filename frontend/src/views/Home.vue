<template>
  <div class="main">This is main page</div>
  <div class="left flex-center">
    <div class="messenger-header-left-content">
      <my-dropdown>
        <template v-slot:target>
          <div class="username">Usernmae</div>
        </template>
        <template v-slot:content>
          <ul>
            <li @click="logout">
              <span class="button">
                <i class="tiny left material-icons">mode_edit</i>
                Update
              </span>
            </li>
          </ul>
        </template>
      </my-dropdown>

      |
      <span> {{ filteredDate }}</span>
    </div>
  </div>
</template>

<script>
import MyDropdown from "@/components/UI/MyDropdown"
export default {
  name: "Home",
  components: { MyDropdown },
  methods: {},
}
</script>

<style scoped></style>
