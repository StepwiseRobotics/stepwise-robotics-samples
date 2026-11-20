"""クラウドGPUの月額費用をざっくり見積もる。

料金は変わるため、実際の単価は各サービスの料金ページで確認して引数に渡す。
"""

from dataclasses import dataclass

HOURS_PER_MONTH = 730  # 1か月の平均時間（24 × 365 ÷ 12）


@dataclass(frozen=True)
class CostEstimate:
    """月額費用の内訳（単位：米ドル）。"""

    compute: float
    storage: float

    @property
    def total(self) -> float:
        return self.compute + self.storage


def estimate_monthly_cost(
    hourly_rate: float,
    hours_running: float,
    storage_gb: float = 0.0,
    storage_rate_per_gb_month: float = 0.0,
) -> CostEstimate:
    """起動時間とディスク容量から、月額の費用を見積もる。

    Args:
        hourly_rate: インスタンスの1時間あたりの料金（米ドル）。
        hours_running: 1か月に起動している時間。停止中は課金されない。
        storage_gb: ディスク容量（GB）。停止中も課金される。
        storage_rate_per_gb_month: ディスクの1GBあたりの月額料金（米ドル）。

    Returns:
        計算時間とストレージの内訳。
    """
    for name, value in {
        "hourly_rate": hourly_rate,
        "hours_running": hours_running,
        "storage_gb": storage_gb,
        "storage_rate_per_gb_month": storage_rate_per_gb_month,
    }.items():
        if value < 0:
            raise ValueError(f"{name} must be non-negative, got {value}")
    if hours_running > HOURS_PER_MONTH:
        raise ValueError(f"hours_running must be <= {HOURS_PER_MONTH}, got {hours_running}")

    return CostEstimate(
        compute=hourly_rate * hours_running,
        storage=storage_gb * storage_rate_per_gb_month,
    )


def forgotten_stop_cost(hourly_rate: float) -> float:
    """停止し忘れて1か月起動しっぱなしにした場合の計算費用（米ドル）。"""
    if hourly_rate < 0:
        raise ValueError(f"hourly_rate must be non-negative, got {hourly_rate}")
    return hourly_rate * HOURS_PER_MONTH
