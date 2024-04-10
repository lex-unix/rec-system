import type { issueTypes } from './data/issue-types';

export type User = {
  id: number;
  fullName: string;
  email: string;
};

export type IssueType = keyof typeof issueTypes;

export type Issue = {
  id: number;
  subject: string;
  description: string;
  type: IssueType;
  userId: number;
};
