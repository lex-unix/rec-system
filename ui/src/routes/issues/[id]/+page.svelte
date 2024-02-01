<script lang="ts">
  import type { Info } from '$components/IssueInfo.svelte';
  import {
    InfoIcon,
    CheckCircle2Icon,
    MoreHorizontalIcon,
    Trash2Icon,
    XCircleIcon
  } from 'lucide-svelte';
  import {
    IssueInfo,
    Popover,
    PopoverTrigger,
    PopoverContent,
    Dropdown,
    DropdownMenu,
    DropdownTrigger,
    DropdownItem,
    Dialog,
    DialogContent,
    DialogTitle,
    DialogDescription,
    DialogClose,
    Button,
    RatingSlider,
    Label,
    Textarea
  } from '$components';
  import { page } from '$app/stores';
  import { issues } from '$lib';
  import { goto } from '$app/navigation';

  let rating: number;
  let review: string = '';
  let dialog: Dialog;

  $: issue = $issues.find(
    ({ id }) => id === parseInt($page.params.id)
  ) as unknown as Info;

  function del() {
    goto('/issues');
    $issues = $issues.filter(c => c.id !== parseInt($page.params.id));
  }

  function resolve() {
    dialog.dismiss();
  }

  function reset() {
    review = '';
  }
</script>

<div class="h-full w-full overflow-hidden">
  <div
    class="relative flex h-20 items-center justify-between border-b border-navy-200/10 px-4"
  >
    <h1 class="w-full text-center text-lg font-medium capitalize">
      {issue?.type}
    </h1>
    <div class="absolute inset-y-0 right-4 pl-5">
      <div class="flex h-full items-center gap-5">
        <Popover>
          <PopoverTrigger class="rounded-full p-2">
            <InfoIcon slot="icon" class="square-5" />
          </PopoverTrigger>
          <PopoverContent>
            <IssueInfo info={issue} />
          </PopoverContent>
        </Popover>
        <Dropdown>
          <DropdownTrigger class="rounded-full p-2">
            <MoreHorizontalIcon class="square-5" />
          </DropdownTrigger>
          <DropdownMenu>
            <DropdownItem on:select={() => dialog.show()}>
              <CheckCircle2Icon class="mr-3 square-5" />
              Mark resolved
            </DropdownItem>
            <DropdownItem on:select={del}>
              <Trash2Icon class="mr-3 square-5" />
              Delete ticket
            </DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </div>
    </div>
  </div>
  <div class="hidden h-full w-full place-items-center lg:grid">
    Chat Placeholder
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
      <Button on:click={() => dialog.dismiss()}>
        <XCircleIcon slot="icon" class="square-4" />
        Dismiss
      </Button>
      <Button on:click={resolve}>
        <CheckCircle2Icon slot="icon" class="square-4" />
        Resolve
      </Button>
    </div>
    <DialogClose />
  </DialogContent>
</Dialog>
