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
  import type { SocketData, Chat } from '$lib/types';
  import { issue } from '$lib/stores';
  import { createSocket } from '$lib/ws';
  import {
    fetchChat,
    fetchCustomerIssue,
    createFeedback,
    changeIssueStatus,
    changeOperatoravAilability
  } from '$lib/api-utils';
  import { useChatbot } from '$lib/stores';
  import {
    CHAT_LOADED_TOAST_ERROR_MSG,
    ISSUE_LOADED_TOAST_ERROR_MSG,
    ISSUE_RESOLVED_TOAST_MSG,
    ISSUE_RESOLVED_TOAST_ERROR_MSG
  } from '$lib/toast-messages';

  let rating: number;
  let review: string = '';
  let dialog: Dialog;
  let messages: SocketData[] = [];
  let socket: WebSocket;
  let chat: Chat;

  onDestroy(() => {
    socket && socket.close();
  });

  $: {
    loadChat($page.params.id);
    loadIssue($page.params.id);
  }

  $: {
    setupSocket($page.params.id, $useChatbot);
  }

  async function loadIssue(issueId: string) {
    const response = await fetchCustomerIssue(issueId);
    if (!response.ok) {
      addToast(ISSUE_LOADED_TOAST_ERROR_MSG);
      return;
    }
    $issue = response.data;
  }

  async function loadChat(issueId: string) {
    const response = await fetchChat(issueId);
    if (!response.ok) {
      addToast(CHAT_LOADED_TOAST_ERROR_MSG);
      return;
    }
    chat = response.data;
    messages = chat.messages.map(m => ({
      message: m.content,
      user_id: m.sender_id,
      created_at: new Date(m.created_at)
    }));
  }

  function setupSocket(issueId: string, useChatbot: boolean) {
    if (socket) {
      socket.close();
    }

    socket = createSocket(`chats/ws/${issueId}?chat_bot=${useChatbot}`);
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
    const issueId = $page.params.id;
    let ok = true;
    {
      const body = JSON.stringify({ rating });
      const response = await createFeedback(issueId, body);
      ok = response.ok;
    }

    {
      const body = JSON.stringify({ status: 'closed' });
      const response = await changeIssueStatus(issueId, body);
      ok = response.ok;
    }

    {
      const body = JSON.stringify({ availability: true });
      const response = await changeOperatoravAilability(
        $issue!.operator.id,
        body
      );
      ok = response.ok;
    }

    if (ok) {
      addToast(ISSUE_RESOLVED_TOAST_MSG);
      issue.updateStatus('closed');
    } else {
      addToast(ISSUE_RESOLVED_TOAST_ERROR_MSG);
    }

    dialog.dismiss();
  }

  function reset() {
    review = '';
  }
</script>

<div class="w-full">
  {#if issue}
    <ChatTopPanel on:resolve={() => dialog.show()} />
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
    <DialogTitle slot="title">Позначте вашу заявку як вирішену</DialogTitle>
    <DialogDescription slot="description">
      Розкажіть нам про свій досвід. Це допоможе покращити наше обслуговування
      клієнтів.
    </DialogDescription>
    <div class="space-y-4">
      <div class="space-y-1">
        <Label for="rating">Рейтинг:</Label>
        <RatingSlider bind:rating />
      </div>
      <div class="space-y-1">
        <Label for="review">Залишити відгук:</Label>
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
        Скасувати
      </Button>
      <Button on:click={resolve} leftIcon={CheckCircle2Icon}>Вирішити</Button>
    </div>
    <DialogClose />
  </DialogContent>
</Dialog>
