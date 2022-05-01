import instance from "@/api/instance"
import authModule from "@/api/auth"
import userModule from "@/api/user"

export default {
  auth: authModule(instance),
  user: userModule(instance),
}
