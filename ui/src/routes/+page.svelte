<script lang="ts">
	import { ticketTypes } from '$lib';
	import { goto } from '$app/navigation';
	import { AirVent } from 'lucide-svelte';
	import {
		Select,
		SelectTrigger,
		SelectMenu,
		SelectItem,
		SelectLabel,
		Input,
		Label,
		Textarea,
		Dialog,
		DialogTrigger,
		DialogTitle,
		DialogContent,
		DialogDescription,
		DialogClose
	} from '$components';

	let selectedType = '';
	let issueSubject = '';
	let issueDescription = '';

	function submit(
		e: SubmitEvent & {
			currentTarget: EventTarget & HTMLFormElement;
		}
	) {
		e.currentTarget.reset();
		goto('/chat');
	}
</script>

<div class="mx-auto max-w-3xl pt-10">
	<form
		on:submit|preventDefault={submit}
		class="space-y-5 rounded-md border border-navy-200/10 p-8 shadow-xl"
	>
		<fieldset class="">
			<Select bind:selected={selectedType}>
				<SelectLabel>Issue Type</SelectLabel>
				<SelectTrigger label="Select issue type" />
				<SelectMenu>
					{#each Object.entries(ticketTypes) as [value, label]}
						<SelectItem {label} {value} />
					{/each}
				</SelectMenu>
			</Select>
		</fieldset>
		<fieldset>
			<Label htmlFor="issueSubject">Issue Subject</Label>
			<Input
				bind:value={issueSubject}
				id="issue-subject"
				name="issueSubject"
				required
			/>
		</fieldset>
		<fieldset>
			<Label htmlFor="issue-description">Issue Description</Label>
			<Textarea
				id="issue-description"
				name="issueDescription"
				required
				bind:value={issueDescription}
			/>
		</fieldset>
		<div class="mt-10">
			<button
				class="rounded-md border border-navy-200/10 bg-navy-800 px-3 py-2 hover:border-navy-200/25"
			>
				Proceed
			</button>
		</div>
	</form>
	<div class="mt-10">
		<Dialog size="md">
			<DialogTrigger>
				<AirVent slot="icon" class="square-4" />
				Open dialog
			</DialogTrigger>
			<DialogContent>
				<DialogTitle slot="title">My dialog title</DialogTitle>
				<DialogDescription slot="description">
					Small description of what's goind on here
				</DialogDescription>
				<div class="max-h-[560px] overflow-y-auto">
					<ul class="list-disc">
						<!-- eslint-disable-next-line @typescript-eslint/no-unused-vars --->
						{#each Array(50) as _, i}
							<li>{i}</li>
						{/each}
					</ul>
				</div>
				<DialogClose />
			</DialogContent>
		</Dialog>
	</div>
</div>
