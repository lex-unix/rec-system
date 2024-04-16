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
  import type { SocketData, Issue } from '$lib/types';
  import { createSocket } from '$lib/ws';
  import { fetchChat, fetchIssue } from '$lib/api-utils';

  let issue: Issue | undefined = undefined;
  let rating: number;
  let review: string = '';
  let dialog: Dialog;
  let messages: SocketData[] = [];
  let socket: WebSocket;

  onDestroy(() => {
    if (socket) {
      socket.close();
    }
  });

  $: issueId = $page.params.id;

  $: {
    loadMessages(issueId);
    loadChat(issueId);
    setupSocket(issueId);
  }

  async function loadChat(issueId: string) {
    const response = await fetchIssue(issueId);
    if (!response.ok) return;
    issue = response.data;
  }

  async function loadMessages(issueId: string) {
    const response = await fetchChat(issueId);
    if (!response.ok) return;
    messages =
      response.data.messages.map(m => ({
        message: m.text,
        userId: m.senderId
      })) || [];
    console.log(messages);
  }

  function setupSocket(issueId: string) {
    if (socket) {
      socket.close();
    }

    socket = createSocket(`chats/ws/${issueId}`);
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
        userId: $user?.id as number
      };
      messages = [...messages, message];
    } else {
      console.log('skill issue');
    }
  }

  function resolve() {
    addToast({
      data: {
        title: 'Issue resolved',
        description: 'Issue is now closed. Thank you for your feedback'
      }
    });
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
      {#each messages as msg}
        <ChatMessage me={msg.userId === $user?.id} date={new Date()}>
          {msg.message}
        </ChatMessage>
      {/each}
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
