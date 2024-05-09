import { type Issue, type IssueStatus, type User } from './types';
import { writable } from 'svelte/store';

export const user = writable<User | undefined>(undefined);

export const useChatbot = writable(true);

function createIssuesStore() {
  const { subscribe, set, update } = writable<Issue[]>([]);

  return {
    subscribe,
    set: (issues: Issue[]) => set(issues),
    remove: (id: number) => update(issues => issues.filter(i => i.id !== id)),
    add: (issue: Issue) => update(issues => [...issues, issue]),
    reset: () => set([])
  };
}

function createIssueStore() {
  const { subscribe, set, update } = writable<Issue | undefined>(undefined);

  return {
    subscribe,
    set: (issue: Issue) => set(issue),
    reset: () => set(undefined),
    updateStatus: (status: IssueStatus) => {
      update(i => i && { ...i, status: status });
    }
  };
}

export const issues = createIssuesStore();
export const issue = createIssueStore();
