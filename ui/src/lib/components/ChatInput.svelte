<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  let value: string;

  const dispatch = createEventDispatcher();

  function send() {
    if (!value) return;

    dispatch('send', { message: value });
    value = '';
  }
</script>

<div class="absolute inset-x-0 bottom-0 h-[120px]">
  <div class="relative border-t border-navy-200/10 p-10">
    <form on:submit|preventDefault={send}>
      <input
        bind:value
        type="text"
        placeholder="Type message..."
        class="w-full bg-navy-900 focus:outline-none"
      />
    </form>
  </div>
</div>
