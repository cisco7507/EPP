"use client";

import { useState, useEffect } from 'react';

interface RegistryProfile {
  id: number;
  name: string;
}

interface DomainCheckResponse {
  availability: boolean;
  request_xml: string;
  response_xml: string;
}

export default function DomainCheckForm() {
  const [profiles, setProfiles] = useState<RegistryProfile[]>([]);
  const [selectedProfile, setSelectedProfile] = useState('');
  const [domainName, setDomainName] = useState('');
  const [result, setResult] = useState<DomainCheckResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchProfiles() {
      const res = await fetch('/api/profiles');
      const data = await res.json();
      setProfiles(data);
      if (data.length > 0) {
        setSelectedProfile(data[0].id.toString());
      }
    }
    fetchProfiles();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResult(null);
    const res = await fetch('/api/domains/check', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        domain_name: domainName,
        profile_id: parseInt(selectedProfile),
      }),
    });
    const data = await res.json();
    setResult(data);
    setIsLoading(false);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="profile" className="block text-gray-700 font-bold mb-2">
            Registry Profile
          </label>
          <select
            id="profile"
            value={selectedProfile}
            onChange={(e) => setSelectedProfile(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          >
            {profiles.map((profile) => (
              <option key={profile.id} value={profile.id}>
                {profile.name}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label htmlFor="domainName" className="block text-gray-700 font-bold mb-2">
            Domain Name
          </label>
          <input
            type="text"
            id="domainName"
            value={domainName}
            onChange={(e) => setDomainName(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          disabled={isLoading}
        >
          {isLoading ? 'Checking...' : 'Check Domain'}
        </button>
      </form>

      {result && (
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-2">Result</h2>
          <p>
            The domain <span className="font-mono">{domainName}</span> is{' '}
            {result.availability ? (
              <span className="text-green-600 font-bold">Available</span>
            ) : (
              <span className="text-red-600 font-bold">Not Available</span>
            )}
          </p>

          <div className="mt-4">
            <h3 className="text-lg font-bold">Request XML</h3>
            <pre className="bg-gray-100 p-4 rounded mt-2">
              <code>{result.request_xml}</code>
            </pre>
          </div>

          <div className="mt-4">
            <h3 className="text-lg font-bold">Response XML</h3>
            <pre className="bg-gray-100 p-4 rounded mt-2">
              <code>{result.response_xml}</code>
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
