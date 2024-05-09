<script lang="ts">
  import { CheckCircle2Icon, XCircleIcon } from 'lucide-svelte';
  import {
    Dialog,
    DialogContent,
    DialogTitle,
    DialogDescription,
    DialogClose,
    Button,
    RatingSlider,
    Label,
    Textarea,
    ChatMessage,
    ChatInput,
    ChatTopPanel
  } from '$components';
  import { addToast } from '$components/Toaster.svelte';
  import { onDestroy } from 'svelte';
  import { user } from '$lib/stores';
  import { page } from '$app/stores';
  import type { SocketData, Issue, Chat } from '$lib/types';
  import { createSocket } from '$lib/ws';
  import {
    fetchChat,
    fetchCustomerIssue,
    createFeedback
  } from '$lib/api-utils';
  import { useChatbot } from '$lib/stores';

  let rating: number;
  let review: string = '';
  let dialog: Dialog;
  let messages: SocketData[] = [];
  let socket: WebSocket;
  let chat: Chat;
  let issue: Issue;

  onDestroy(() => {
    if (socket) {
      socket.close();
    }
  });

  $: issueId = $page.params.id;

  $: {
    loadChat(issueId);
    loadIssue(issueId);
    setupSocket(issueId);
  }

  $: {
    if ($useChatbot || !$useChatbot) {
      socket.close();
      setupSocket(issueId);
    }
  }

  async function loadIssue(issueId: string) {
    const response = await fetchCustomerIssue(issueId);
    if (!response.ok) return;
    issue = response.data;
  }

  async function loadChat(issueId: string) {
    const response = await fetchChat(issueId);
    if (!response.ok) return;
    chat = response.data;
    messages = chat.messages.map(m => ({
      message: m.content,
      user_id: m.sender_id,
      created_at: new Date(m.created_at)
    }));
  }

  function setupSocket(issueId: string) {
    if (socket) {
      socket.close();
    }

    socket = createSocket(`chats/ws/${issueId}?chat_bot=${$useChatbot}`);
    socket.onmessage = event => {
      const data: SocketData = JSON.parse(event.data);
      messages = [...messages, data];
    };
    socket.onopen = () => console.log('WebSocket connected');
    socket.onclose = () => console.log('WebSocket disconnected');
  }

  function send(e: CustomEvent<{ message: string }>) {
    if (socket.readyState === WebSocket.OPEN) {
      socket.send(e.detail.message);
      const message: SocketData = {
        message: e.detail.message,
        user_id: $user?.id as number,
        created_at: new Date()
      };
      messages = [...messages, message];
    } else {
      console.log('skill issue');
    }
  }

  async function resolve() {
    const body = JSON.stringify({ rating });
    console.log($page.params.id);
    const response = await createFeedback($page.params.id, body);
    if (response.ok) {
      addToast({
        data: {
          title: 'Issue resolved',
          description: 'Issue is now closed. Thank you for your feedback'
        }
      });
    }
    dialog.dismiss();
  }

  function reset() {
    review = '';
  }
</script>

<div class="w-full">
  {#if issue}
    <ChatTopPanel {issue} on:resolve={() => dialog.show()} />
  {/if}

  <div class="relative h-[calc(100%-80px)] w-full overflow-y-auto">
    <div
      class="flex max-h-[calc(100%-120px)] flex-col gap-4 overflow-y-auto p-4"
    >
      {#if chat}
        {#each messages as msg}
          <ChatMessage me={msg.user_id === $user?.id} date={msg.created_at}>
            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
            {@html msg.message}
          </ChatMessage>
        {/each}
      {/if}
    </div>
    <ChatInput on:send={send} />
  </div>
</div>

<Dialog bind:this={dialog} on:close={reset} size="md">
  <DialogContent>
    <DialogTitle slot="title">Mark your issue as resolved</DialogTitle>
    <DialogDescription slot="description">
      Tell us about your experience. This will help enhance our customer support
      service.
    </DialogDescription>
    <div class="space-y-4">
      <div class="space-y-1">
        <Label for="rating">Rating:</Label>
        <RatingSlider bind:rating />
      </div>
      <div class="space-y-1">
        <Label for="review">Leave a review:</Label>
        <Textarea
          id="review"
          name="review"
          bind:value={review}
          class="w-full max-w-none"
        />
      </div>
    </div>
    <div class="ml-auto mt-5 flex w-full justify-end gap-5">
      <Button on:click={() => dialog.dismiss()} leftIcon={XCircleIcon}>
        Dismiss
      </Button>
      <Button on:click={resolve} leftIcon={CheckCircle2Icon}>Resolve</Button>
    </div>
    <DialogClose />
  </DialogContent>
</Dialog>
