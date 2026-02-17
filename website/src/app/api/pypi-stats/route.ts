export const revalidate = 3600; // cache for 1 hour

export async function GET() {
  try {
    const res = await fetch(
      "https://pypistats.org/api/packages/agentbudget/overall",
      { next: { revalidate: 3600 } }
    );
    const data = await res.json();
    // Sum all "without_mirrors" entries for total real downloads
    let total = 0;
    if (Array.isArray(data?.data)) {
      for (const entry of data.data) {
        if (entry.category === "without_mirrors") {
          total += entry.downloads;
        }
      }
    }
    return Response.json({ downloads: total || null });
  } catch {
    return Response.json({ downloads: null });
  }
}
