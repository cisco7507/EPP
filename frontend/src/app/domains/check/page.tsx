import DomainCheckForm from '@/components/domain-check-form';

export default function DomainCheckPage() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <div className="w-full max-w-2xl">
        <h1 className="text-2xl font-bold mb-4">Domain Check</h1>
        <DomainCheckForm />
      </div>
    </main>
  );
}
