#!/usr/bin/env python3
"""Reconstructed baseline diagnostic model supplied with the research materials.

This uses SimPy, not SeQUeNCe. It preserves the earlier model's parameters and
event flow for transparency. It is not a substitute for the SeQUeNCe experiment
described in the manuscript.

Run:
    python src/baseline_diagnostic_simpy.py --seed 2026 --horizon-s 10
"""
from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import simpy

ROOT = Path(__file__).resolve().parents[1]

LINK_LENGTH_KM = 10.0
ATTENUATION_DB_PER_KM = 0.2
P_GEN_BASE = 1e-5
ATTEMPT_INTERVAL_US = 115.072
MEMORY_CUTOFF_US = 100.0
GENERATION_TRIALS_PER_ATTEMPT = 5
INTERMEDIATE_ROUTERS = 15
ROUTE = ["Node A"] + [f"Router {i}" for i in range(1, INTERMEDIATE_ROUTERS + 1)] + ["Node B"]
HOPS = len(ROUTE) - 1
LOSS_DB = LINK_LENGTH_KM * ATTENUATION_DB_PER_KM
FIBER_TRANSMISSION = 10 ** (-LOSS_DB / 10)
P_SUCCESS_PER_TRIAL = P_GEN_BASE * FIBER_TRANSMISSION


class BaselineRun:
    def __init__(self, env: simpy.Environment, rng: random.Random):
        self.env = env
        self.rng = rng
        self.attempts = 0
        self.generated = 0
        self.usable = 0
        self.purged = 0
        self.hop_delays_us: list[float] = []
        self.events: list[dict] = []

    def run(self):
        """Attempt generation; then forward each generated resource hop by hop."""
        while True:
            yield self.env.timeout(ATTEMPT_INTERVAL_US)
            for trial_index in range(GENERATION_TRIALS_PER_ATTEMPT):
                self.attempts += 1
                if self.rng.random() >= P_SUCCESS_PER_TRIAL:
                    continue

                self.generated += 1
                resource_id = self.generated
                created_us = float(self.env.now)
                for hop_index in range(HOPS):
                    delay = self.rng.uniform(50.0, 150.0)
                    self.hop_delays_us.append(delay)
                    yield self.env.timeout(delay)

                age_us = float(self.env.now) - created_us
                expired = age_us > MEMORY_CUTOFF_US
                if expired:
                    self.purged += 1
                else:
                    self.usable += 1
                self.events.append({
                    "resource_id": resource_id,
                    "created_us": created_us,
                    "consumed_us": float(self.env.now),
                    "age_us": age_us,
                    "memory_cutoff_us": MEMORY_CUTOFF_US,
                    "outcome": "purged" if expired else "usable",
                    "hop_count": HOPS,
                })


def topology_edges(topology: str, nodes: list[str]):
    if topology == "line":
        return list(zip(nodes, nodes[1:]))
    if topology == "ring":
        return list(zip(nodes, nodes[1:] + nodes[:1]))
    if topology == "star":
        return [(nodes[0], node) for node in nodes[1:]]
    if topology == "mesh":
        return [(nodes[i], nodes[j]) for i in range(len(nodes)) for j in range(i + 1, len(nodes))]
    if topology == "tree":
        return [(nodes[(i - 1) // 2], nodes[i]) for i in range(1, len(nodes))]
    raise ValueError(f"Unsupported topology: {topology}")


def write_topology_figure(path: Path):
    topologies = ["line", "star", "ring", "mesh", "tree"]
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    nodes = ROUTE
    for ax, topology in zip(axes.flat, topologies):
        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(topology_edges(topology, nodes))
        if topology == "line":
            positions = {node: (i, 0) for i, node in enumerate(nodes)}
        elif topology == "ring":
            positions = nx.circular_layout(graph)
        elif topology == "star":
            positions = nx.spring_layout(graph, seed=11)
        elif topology == "tree":
            positions = nx.spring_layout(graph, seed=11)
        else:
            positions = nx.spring_layout(graph, seed=11)
        endpoint_colours = ["#2a9d8f" if n in (nodes[0], nodes[-1]) else "#f4a261" for n in nodes]
        nx.draw_networkx(
            graph, positions, ax=ax, with_labels=False, node_size=90,
            node_color=endpoint_colours, edge_color="#52748a", width=0.7
        )
        ax.set_title(f"{topology.title()} topology")
        ax.axis("off")
    axes.flat[-1].axis("off")
    fig.suptitle("Quantum-network topology configurations (illustrative)", fontsize=14)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def write_run_outputs(run: BaselineRun, seed: int, horizon_s: float, output_dir: Path):
    data_dir = output_dir / "data" / "processed"
    figure_dir = output_dir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    summary_path = data_dir / "baseline_diagnostic_summary.csv"
    summary = {
        "simulator": "SimPy baseline reconstruction (not SeQUeNCe)",
        "seed": seed,
        "horizon_s": horizon_s,
        "intermediate_routers": INTERMEDIATE_ROUTERS,
        "hops": HOPS,
        "link_length_km": LINK_LENGTH_KM,
        "attenuation_db_per_km": ATTENUATION_DB_PER_KM,
        "fiber_transmission_factor": FIBER_TRANSMISSION,
        "generation_trials_per_attempt": GENERATION_TRIALS_PER_ATTEMPT,
        "generation_probability_per_trial": P_SUCCESS_PER_TRIAL,
        "memory_cutoff_us": MEMORY_CUTOFF_US,
        "qubit_attempts": run.attempts,
        "generated_resources": run.generated,
        "usable_end_to_end_resources": run.usable,
        "purged_resources": run.purged,
        "usable_rate_percent": 100 * run.usable / run.generated if run.generated else 0.0,
    }
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    events_path = data_dir / "baseline_resource_events.csv"
    with events_path.open("w", newline="", encoding="utf-8") as handle:
        columns = ["resource_id", "created_us", "consumed_us", "age_us",
                   "memory_cutoff_us", "outcome", "hop_count"]
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(run.events)

    delays_path = data_dir / "baseline_hop_delays.csv"
    with delays_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["hop_delay_us"])
        writer.writerows([[x] for x in run.hop_delays_us])

    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    if run.hop_delays_us:
        ax.hist(run.hop_delays_us, bins=10, edgecolor="white")
    else:
        ax.text(0.5, 0.5, "No generated resource; no hop transfers", ha="center", va="center")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    ax.set_xlabel("Hop delay (μs)")
    ax.set_ylabel("Transfer count")
    ax.set_title("Hop-by-hop delay samples")
    fig.tight_layout()
    fig.savefig(figure_dir / "baseline_hop_delay_histogram.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    ax.bar(["Usable", "Purged"], [run.usable, run.purged])
    ax.set_ylabel("Generated resources")
    ax.set_title("Baseline resource outcomes")
    fig.tight_layout()
    fig.savefig(figure_dir / "baseline_resource_outcomes.png", dpi=180)
    plt.close(fig)

    write_topology_figure(figure_dir / "network_topologies.png")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--horizon-s", type=float, default=10.0)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    if args.horizon_s <= 0:
        parser.error("--horizon-s must be positive")

    rng = random.Random(args.seed)
    env = simpy.Environment()
    run = BaselineRun(env, rng)
    env.process(run.run())
    env.run(until=args.horizon_s * 1_000_000)
    summary = write_run_outputs(run, args.seed, args.horizon_s, args.output_dir)

    print("BASELINE DIAGNOSTIC RECONSTRUCTION (SimPy, not SeQUeNCe)")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print("Outputs written under data/processed/ and figures/.")


if __name__ == "__main__":
    main()
