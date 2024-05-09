<script lang="ts">
  import {
    InfoIcon,
    CheckCircle2Icon,
    MoreHorizontalIcon,
    Trash2Icon,
    CogIcon
  } from 'lucide-svelte';
  import {
    IssueInfo,
    Switch,
    SwitchButton,
    SwitchLabel,
    Popover,
    PopoverTrigger,
    PopoverContent,
    Dropdown,
    DropdownMenu,
    DropdownTrigger,
    DropdownItem,
    MobileIssuesDrawer
  } from '$components';
  import { issueType } from '$lib/issues';
  import { goto } from '$app/navigation';
  import { createEventDispatcher } from 'svelte';
  import { addToast } from './Toaster.svelte';
  import type { Issue } from '$lib/types';
  import { useChatbot } from '$lib/stores';

  export let issue: Issue;

  const dispatch = createEventDispatcher();

  function deleteIssue() {
    goto('/issues');
    // $issues = $issues.filter(c => c.id !== parseInt($page.params.id));
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

  $: console.log($useChatbot);
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
    {issueType[issue.type]}
  </h1>

  <div class="absolute inset-y-0 right-4 pl-5">
    <div class="flex h-full items-center gap-5">
      <Popover>
        <PopoverTrigger class="rounded-full p-2">
          <CogIcon slot="icon" class="square-5" />
        </PopoverTrigger>
        <PopoverContent class="min-w-[300px]">
          <div>
            <h2 class="text-center text-lg font-medium">Chat settings</h2>
            <div class="pt-8">
              <Switch enabled={useChatbot}>
                <div class="flex items-center gap-3">
                  <SwitchLabel>Use chatbot?</SwitchLabel>
                  <SwitchButton />
                </div>
              </Switch>
            </div>
          </div>
        </PopoverContent>
      </Popover>
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
