import { parse } from 'tldts';

export interface ParsedUrlFeatures {
  protocol: string;
  hostname: string;
  port: string;
  pathname: string;
  query: string;
  hash: string;
  isIpAddress: boolean;
  tld: string;
  registrableDomain: string;
  subdomain: string;
}

export function parseUrl(urlString: string): ParsedUrlFeatures | null {
  try {
    let normalized = urlString.trim().toLowerCase();
    if (!normalized.startsWith('http')) {
      normalized = 'https://' + normalized;
    }
    const urlObj = new URL(normalized);
    const tldInfo = parse(urlObj.hostname);
    const isIp = /^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$/.test(urlObj.hostname);

    return {
      protocol: urlObj.protocol.replace(':', ''),
      hostname: urlObj.hostname,
      port: urlObj.port || (urlObj.protocol === 'https:' ? '443' : '80'),
      pathname: urlObj.pathname,
      query: urlObj.search,
      hash: urlObj.hash,
      isIpAddress: isIp,
      tld: tldInfo.publicSuffix || '',
      registrableDomain: tldInfo.domain || urlObj.hostname,
      subdomain: tldInfo.subdomain || ''
    };
  } catch (error) {
    return null;
  }
}
