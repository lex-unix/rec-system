<script lang="ts">
  import { page } from '$app/stores';
  import { issues as initIssues, issueTypes } from '$lib';
  import {
    Button,
    Input,
    Label,
    SearchBar,
    Select,
    SelectItem,
    SelectLabel,
    SelectMenu,
    SelectTrigger,
    Textarea
  } from '$components';
  import {
    ArrowRightCircleIcon,
    PlusCircleIcon,
    XOctagonIcon
  } from 'lucide-svelte';
  import {
    Dialog,
    DialogTrigger,
    DialogTitle,
    DialogDescription,
    DialogContent,
    DialogClose
  } from '$components';

  let issueSubject = '';
  let issueType = '';
  let issueDescription = '';
  let dialog: Dialog;

  $: issues = $initIssues;

  function filter(e: CustomEvent<{ search: string }>) {
    issues = $initIssues.filter(c =>
      c.type.toLowerCase().includes(e.detail.search.toLowerCase())
    );
  }

  function reset() {
    issueSubject = '';
    issueDescription = '';
  }

  function add() {
    dialog.dismiss();
  }

  function cancel() {
    dialog.dismiss();
  }
</script>

<div class="flex h-screen max-h-screen">
  <div
    class="relative hidden h-full shrink-0 flex-col border-r border-navy-200/10 md:flex md:w-[320px] md:max-w-[320px] md:flex-col lg:w-[400px] lg:max-w-[400px]"
  >
    <div class="flex h-20 w-full items-center border-b border-navy-200/10 px-5">
      <SearchBar on:search={filter} />
    </div>
    <ul
      class="chat-list flex-1 list-none space-y-1 overflow-y-auto px-5 pb-4 pt-4"
    >
      {#each issues as { id, type, description }}
        <li>
          <a
            href="/issues/{id}"
            class="line-clamp-1 block w-full rounded-md px-5 py-3 hover:bg-navy-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#479EFA]"
            class:active={$page.params.id
              ? parseInt($page.params.id) === id
              : false}
          >
            <p class="capitalize">
              {type}
            </p>
            <p class="line-clamp-1 text-navy-400">{description}</p>
          </a>
        </li>
      {/each}
    </ul>
    <div class="mt-auto h-20 max-h-20 border-t border-t-navy-200/10">
      <div class="flex h-full items-center justify-center px-5">
        <Dialog bind:this={dialog} on:close={reset}>
          <DialogTrigger class="flex w-full items-center justify-center">
            <PlusCircleIcon slot="icon" class="square-4" />
            New issue
          </DialogTrigger>
          <DialogContent>
            <DialogTitle slot="title">Create new issue</DialogTitle>
            <DialogDescription slot="description">
              Start by filling out the simple form.
            </DialogDescription>
            <div class="max-w-none space-y-5">
              <div class="space-y-1">
                <Select bind:selected={issueType}>
                  <SelectLabel>Issue type</SelectLabel>
                  <SelectTrigger
                    label="Select issue type"
                    class="w-full max-w-none"
                  />
                  <SelectMenu>
                    {#each Object.entries(issueTypes) as [value, label]}
                      <SelectItem {label} {value} />
                    {/each}
                  </SelectMenu>
                </Select>
              </div>
              <div class="space-y-1">
                <Label for="issue-subject">Issue subject:</Label>
                <Input
                  id="issue-subject"
                  name="issueSubject"
                  bind:value={issueSubject}
                  class="w-full max-w-none"
                />
              </div>
              <div class="space-y-1">
                <Label for="">Issue description:</Label>
                <Textarea
                  id="issue-description"
                  name="issueDescription"
                  bind:value={issueDescription}
                  class="w-full max-w-none"
                />
              </div>
            </div>
            <div class="mt-5">
              <div class="flex items-center justify-end gap-4">
                <Button on:click={cancel}>
                  <XOctagonIcon slot="icon" class="square-4" />
                  Cancel
                </Button>
                <Button on:click={add}>
                  <ArrowRightCircleIcon slot="icon" class="square-4" />
                  Procced
                </Button>
              </div>
            </div>
            <DialogClose />
          </DialogContent>
        </Dialog>
      </div>
    </div>
  </div>
  <slot />
</div>

<style lang="postcss">
  .active {
    background: theme(colors.navy.800);
  }

  .chat-list {
    max-height: calc(100% - theme(spacing.20));
  }
</style>
