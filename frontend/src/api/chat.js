export default function (instance) {
  return {
    getChats() {
      return instance.get("api/v1/chats/list")
    },
    getSearchedChats(title) {
      return instance.get(`api/v1/chats/list/${title}`)
    },
    getChatMessages(chatId) {
      return instance.get(`api/v1/chats/${chatId}`)
    },
    sendMessage(chatId, payload) {
      return instance.post(`api/v1/chats/${chatId}/send`, payload)
    },
  }
}
