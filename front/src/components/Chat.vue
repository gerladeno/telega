<template>
    <li>
        <div>Id: {{chat.id}}</div>
        <div>Title: {{chat.title}}</div>
        <div>new Message: {{chat.newMessage}}</div>
    </li>
</template>

<script>
export default {
    props: ['chat']
}
</script>