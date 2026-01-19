"""
EFD Providers Module
Factory pattern for EFD provider selection
"""

from tanzania.efd.providers.base import BaseEFDProvider
from tanzania.efd.providers.vfdplus import VFDPlusProvider
from tanzania.efd.providers.totalvfd import TotalVFDProvider
from tanzania.efd.providers.simplifyvfd import SimplifyVFDProvider


PROVIDERS = {
	"VFDPlus": VFDPlusProvider,
	"TotalVFD": TotalVFDProvider,
	"SimplifyVFD": SimplifyVFDProvider,
}


def get_provider(provider_name):
	"""Get provider class instance by name"""
	if provider_name not in PROVIDERS:
		raise ValueError(f"Unknown EFD provider: {provider_name}")
	return PROVIDERS[provider_name]()
