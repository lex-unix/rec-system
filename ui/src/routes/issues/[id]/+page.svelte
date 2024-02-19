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
  import { messages as initMessage } from '$lib/data/messages';
  import { addToast } from '$components/Toaster.svelte';

  let rating: number;
  let review: string = '';
  let dialog: Dialog;
  let messages = initMessage;

  function send(e: CustomEvent<{ message: string }>) {
    const newMsg = { me: true, date: new Date(), text: e.detail.message };
    messages.push(newMsg);
    messages = messages;
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
  <ChatTopPanel on:resolve={() => dialog.show()} />

  <div class="relative h-[calc(100%-80px)] w-full overflow-y-auto">
    <div
      class="flex max-h-[calc(100%-120px)] flex-col gap-4 overflow-y-auto p-4"
    >
      {#each messages as { me, date, text }}
        <ChatMessage {me} {date}>{text}</ChatMessage>
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
