import { writable } from 'svelte/store';

export const issues = writable([
	{
		id: 1,
		status: 'resolved',
		type: 'refund',
		subject: 'Refund Request',
		description: 'Customer is requesting a refund for their recent purchase.',
		operatorName: 'John Doe',
		averageRating: 4.5,
		totalResolvedIssues: 10
	},
	{
		id: 2,
		status: 'in progress',
		type: 'technical',
		subject: 'Technical Issue',
		description: 'Customer is facing difficulties accessing the website.',
		operatorName: 'Jane Smith',
		averageRating: 3.8,
		totalResolvedIssues: 5
	},
	{
		id: 3,
		status: 'resolved',
		type: 'billing',
		subject: 'Billing Discrepancy',
		description:
			'Customer noticed an incorrect charge on their monthly invoice.',
		operatorName: 'Mike Johnson',
		averageRating: 4.2,
		totalResolvedIssues: 15
	},
	{
		id: 4,
		status: 'in progress',
		type: 'product inquiry',
		subject: 'Product Compatibility',
		description:
			'Customer wants to know if the product is compatible with their device.',
		operatorName: 'Sarah Davis',
		averageRating: 4.7,
		totalResolvedIssues: 20
	},
	{
		id: 5,
		status: 'resolved',
		type: 'technical',
		subject: 'Login Issues',
		description: 'Customer is unable to log into their account.',
		operatorName: 'Alex Brooks',
		averageRating: 3.5,
		totalResolvedIssues: 8
	},
	{
		id: 6,
		status: 'resolved',
		type: 'refund',
		subject: 'Refund Request',
		description: 'Customer wants to return the product due to a defect.',
		operatorName: 'Emily Thompson',
		averageRating: 4.8,
		totalResolvedIssues: 13
	},
	{
		id: 7,
		status: 'resolved',
		type: 'product inquiry',
		subject: 'Product Specifications',
		description:
			'Customer needs more information about the product specifications.',
		operatorName: 'David Wilson',
		averageRating: 4.1,
		totalResolvedIssues: 18
	},
	{
		id: 8,
		status: 'in progress',
		type: 'technical',
		subject: 'Website Error',
		description:
			'Customer encountered an error message while browsing the website.',
		operatorName: 'Karen Anderson',
		averageRating: 3.9,
		totalResolvedIssues: 7
	},
	{
		id: 9,
		status: 'resolved',
		type: 'billing',
		subject: 'Payment Confirmation',
		description:
			'Customer wants to confirm if their payment was successfully processed.',
		operatorName: 'Mark Roberts',
		averageRating: 4.4,
		totalResolvedIssues: 12
	},
	{
		id: 10,
		status: 'in progress',
		type: 'cancellation request',
		subject: 'Cancellation Request',
		description: 'Customer wants to cancel their subscription service.',
		operatorName: 'Amy Wilson',
		averageRating: 4.3,
		totalResolvedIssues: 9
	},
	{
		id: 11,
		status: 'resolved',
		type: 'technical',
		subject: 'Video Streaming Quality',
		description: 'Customer is experiencing low video quality while streaming.',
		operatorName: 'Michael Brown',
		averageRating: 4.6,
		totalResolvedIssues: 16
	},
	{
		id: 12,
		status: 'resolved',
		type: 'product inquiry',
		subject: 'Product Availability',
		description: 'Customer wants to know if the product is currently in stock.',
		operatorName: 'Laura Lee',
		averageRating: 4.0,
		totalResolvedIssues: 14
	},
	{
		id: 13,
		status: 'in progress',
		type: 'billing',
		subject: 'Payment Method Update',
		description: 'Customer needs assistance in updating their payment method.',
		operatorName: 'Thomas Clark',
		averageRating: 4.2,
		totalResolvedIssues: 11
	}
]);
