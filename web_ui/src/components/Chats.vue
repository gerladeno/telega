<template>
    <div>
        <ul>
            <Chat 
                v-for="chat in chats"
                v-bind:key="chat.id"
                v-bind:chat="chat"
             />
        </ul>
    </div>
</template>

<script>
import Chat from '@/components/Chat'
export default {
    props: ['chats'],
    components:{
        Chat
    }
}
</script>