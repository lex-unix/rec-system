<script lang="ts">
	import { createTabs, melt } from '@melt-ui/svelte';
	import { crossfade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import ResizablePannel from './ResizablePannel.svelte';

	const {
		elements: { root, list, content, trigger },
		states: { value }
	} = createTabs({ defaultValue: 'tab-1' });

	const triggers = [
		{ id: 'tab-1', title: 'Issue' },
		{ id: 'tab-2', title: 'Operator' }
	];

	const [send, receive] = crossfade({
		duration: 200,
		easing: cubicInOut
	});
</script>

<ResizablePannel duration={200}>
	<div use:melt={$root} class="list w-[420px] max-w-xs text-sm">
		<div
			use:melt={$list}
			class="mb-6 flex items-center justify-between overflow-x-auto rounded-md border border-navy-200/10 bg-navy-900 p-1"
			aria-label="Manage your account"
		>
			{#each triggers as triggerItem}
				<button
					use:melt={$trigger(triggerItem.id)}
					class="relative h-8 flex-1 select-none rounded leading-none text-navy-400 transition-colors duration-200 focus:outline-none data-[state=active]:text-navy-50"
				>
					{#if $value === triggerItem.id}
						<div
							in:send={{ key: 'trigger' }}
							out:receive={{ key: 'trigger' }}
							class="absolute inset-0 rounded border border-navy-200/10 bg-navy-800"
						/>
					{/if}
					<span class="absolute inset-0 flex items-center justify-center">
						{triggerItem.title}
					</span>
				</button>
			{/each}
		</div>
		<div use:melt={$content('tab-1')}>
			<h3 class="border-b border-navy-200/10 pb-4 text-lg font-medium">
				Issue details
			</h3>
			<div class="divide-y divide-navy-200/10">
				<div class="space-y-1 py-4">
					<p class="text-navy-400">Issue Status:</p>
					<p class="text-navy-100">In progress</p>
				</div>
				<div class="space-y-1 py-4">
					<p class="text-navy-400">Issue type:</p>
					<p class="text-navy-100">Refund</p>
				</div>
				<div class="space-y-1 py-4">
					<p class="text-navy-400">Issue subject:</p>
					<p class="text-navy-100">Computer not working</p>
				</div>
				<div class="space-y-1 py-4">
					<p class="text-navy-400">Issue description:</p>
					<p class="text-navy-100">
						Consectetur esse aute nulla id aute duis. Cillum in commodo non in
						occaecat ipsum proident.
					</p>
				</div>
			</div>
		</div>
		<div use:melt={$content('tab-2')}>
			<h3 class="border-b border-navy-200/10 pb-4 text-lg font-medium">
				Operator details
			</h3>
			<div class="divide-y divide-navy-200/10">
				<div class="space-y-1 py-4">
					<p class="text-navy-400">Full name:</p>
					<p class="text-navy-100">Bob Martin</p>
				</div>
				<div class="space-y-1 py-4">
					<p class="text-navy-400">Average rating:</p>
					<p class="text-navy-100">4.99</p>
				</div>
				<div class="space-y-1 py-4">
					<p class="text-navy-400">Resolved issues:</p>
					<p class="text-navy-100">420</p>
				</div>
			</div>
		</div>
	</div>
</ResizablePannel>
