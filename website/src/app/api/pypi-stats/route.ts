export const revalidate = 3600; // cache for 1 hour

export async function GET() {
  try {
    const res = await fetch(
      "https://pypistats.org/api/packages/agentbudget/recent",
      { next: { revalidate: 3600 } }
    );
    const data = await res.json();
    return Response.json({ downloads: data?.data?.last_month ?? null });
  } catch {
    return Response.json({ downloads: null });
  }
}
