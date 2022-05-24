import instance from "@/api/instance"
import authModule from "@/api/auth"
import userModule from "@/api/user"
import chatModule from "@/api/chat"

export default {
  auth: authModule(instance),
  user: userModule(instance),
  chat: chatModule(instance),
}
