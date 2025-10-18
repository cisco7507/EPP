"use client";

import { useEffect, useState } from 'react';

interface RegistryProfile {
  id: number;
  name: string;
  host: string;
  port: number;
  username: string;
}

export default function Profiles() {
  const [profiles, setProfiles] = useState<RegistryProfile[]>([]);

  useEffect(() => {
    async function fetchProfiles() {
      const res = await fetch('/api/profiles');
      const data = await res.json();
      setProfiles(data);
    }
    fetchProfiles();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Registry Profiles</h1>
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4">
        Add Profile
      </button>
      <table className="table-auto w-full">
        <thead>
          <tr>
            <th className="px-4 py-2">Name</th>
            <th className="px-4 py-2">Host</th>
            <th className="px-4 py-2">Port</th>
            <th className="px-4 py-2">Username</th>
            <th className="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {profiles.map((profile) => (
            <tr key={profile.id}>
              <td className="border px-4 py-2">{profile.name}</td>
              <td className="border px-4 py-2">{profile.host}</td>
              <td className="border px-4 py-2">{profile.port}</td>
              <td className="border px-4 py-2">{profile.username}</td>
              <td className="border px-4 py-2">
                <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-2 rounded mr-2">
                  Edit
                </button>
                <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded">
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
