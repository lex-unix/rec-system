<script lang="ts">
  import {
    InfoIcon,
    CheckCircle2Icon,
    MoreHorizontalIcon,
    Trash2Icon
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
    MobileIssuesDrawer
  } from '$components';
  import { page } from '$app/stores';
  import { issues } from '$lib';
  import { goto } from '$app/navigation';
  import { createEventDispatcher } from 'svelte';
  import { addToast } from './Toaster.svelte';
  import type { Issue } from '$lib/types';

  export let issue: Issue;

  const dispatch = createEventDispatcher();

  function deleteIssue() {
    goto('/issues');
    $issues = $issues.filter(c => c.id !== parseInt($page.params.id));
    addToast({
      data: {
        title: 'Issue deleted',
        description: 'Issue successfully deleted from your list'
      }
    });
  }

  function resolve() {
    dispatch('resolve');
  }
</script>

<div
  class="relative flex h-20 items-center justify-between border-b border-navy-200/10 px-4"
>
  <div class="absolute inset-y-0 left-4 block md:hidden">
    <div class="flex h-full items-center">
      <MobileIssuesDrawer />
    </div>
  </div>
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
          <IssueInfo {issue} />
        </PopoverContent>
      </Popover>
      <Dropdown>
        <DropdownTrigger class="rounded-full p-2">
          <MoreHorizontalIcon class="square-5" />
        </DropdownTrigger>
        <DropdownMenu>
          <DropdownItem on:select={resolve}>
            <CheckCircle2Icon class="mr-3 square-5" />
            Mark resolved
          </DropdownItem>
          <DropdownItem on:select={deleteIssue}>
            <Trash2Icon class="mr-3 square-5" />
            Delete ticket
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>
    </div>
  </div>
</div>
