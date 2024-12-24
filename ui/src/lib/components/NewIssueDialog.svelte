<script lang="ts">
  import { issueTypes } from '$lib';
  import {
    Button,
    Input,
    Label,
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
  import { createEventDispatcher } from 'svelte';

  let issueSubject = '';
  let issueType = '';
  let issueDescription = '';
  let dialog: Dialog;

  const dispatch = createEventDispatcher();

  function reset() {
    issueSubject = '';
    issueDescription = '';
  }

  function add() {
    dispatch('add', {
      subject: issueSubject,
      type: issueType,
      description: issueDescription
    });
    dialog.dismiss();
  }

  function cancel() {
    dialog.dismiss();
  }
</script>

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
    <form on:submit|preventDefault={add} class="max-w-none space-y-5">
      <div class="space-y-1">
        <Select bind:selected={issueType}>
          <SelectLabel>Issue type</SelectLabel>
          <SelectTrigger label="Select issue type" class="w-full max-w-none" />
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
          required
        />
      </div>
      <div class="space-y-1">
        <Label for="">Issue description:</Label>
        <Textarea
          id="issue-description"
          name="issueDescription"
          bind:value={issueDescription}
          class="w-full max-w-none"
          required
        />
      </div>
      <div class="mt-5">
        <div class="flex items-center justify-end gap-4">
          <Button on:click={cancel} rightIcon={XOctagonIcon}>Cancel</Button>
          <Button type="submit" rightIcon={ArrowRightCircleIcon}>
            Procced
          </Button>
        </div>
      </div>
    </form>
    <DialogClose />
  </DialogContent>
</Dialog>
