import math


class StochasticPathSolver:
    def __init__(self, row_player_mixed_ne: float, col_player_mixed_ne: float, sample_len: int):
        self.col_player_mixed_NE = col_player_mixed_ne
        self.row_player_mixed_NE = row_player_mixed_ne
        self.sample_len = sample_len

    @staticmethod
    def num_of_combinations(n: int, k: int) -> float:
        return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

    @staticmethod
    def probability_of_sample(qty_a_sample: int, qty_b_sample: int,
                              qty_a_mem: int, qty_b_mem: int , memory_len: int) -> float:
        num_of_comb = StochasticPathSolver.num_of_combinations
        sample_len = qty_a_sample + qty_b_sample
        combs_a_in_sample = num_of_comb(n=qty_a_mem, k=qty_a_sample)
        combs_b_in_sample = num_of_comb(n=qty_b_mem, k=qty_b_sample)
        combs_sample_in_mem = num_of_comb(n=memory_len, k=sample_len)
        prob_of_sample = combs_a_in_sample*combs_b_in_sample/combs_sample_in_mem
        return prob_of_sample

    def strategy_probability(self, path1: str, path2: str, mixed_ne_prob: float) -> float:
        memory = [path1.count('A'), path1.count('B')]  # [0] = qty of A, [1] = qty of B
        memory_len = len(path1)
        if path2[-1].lower() == 'a':  # whether the next played strategy is A
            next_a = True
        else:
            next_a = False
        # count combinations and drop odd ones
        combination_table = []
        for a in range(0, self.sample_len + 1):
            for b in range(0, self.sample_len + 1):
                if (a + b) != self.sample_len:  # preserve sample length
                    pass
                elif a > memory[0] or b > memory[1]:  # both a and b have to be smaller than their qty.
                    pass
                else:
                    combination_table.append([a, b])
        print("Возможные выборки: ", combination_table)

        appropriate_samples = []
        # find appropriate strategies
        for element in combination_table:
            sample_prob = element[0] / sum(element)
            # if sample does not provide an appropriate expected next strategy, drop it
            if next_a: # then, if NE_prob > sample_prob, player plays A (too many times played B)
                if mixed_ne_prob > sample_prob:
                    appropriate_samples.append(element)
            else: # then, if NE_prob < sample_prob, player plays B (too many times played A)
                if mixed_ne_prob < sample_prob:
                    appropriate_samples.append(element)

        # calculate probabilities
        probs = []
        print("Подходящие выборки и их вероятности:")
        for subset in appropriate_samples:
            prob = self.probability_of_sample(qty_a_sample=subset[0], qty_b_sample=subset[1],
                                              qty_a_mem=memory[0],qty_b_mem=memory[1], memory_len=memory_len)
            probs.append(prob)
            print('A'*subset[0] + 'B'*subset[1] + ', p = {}'.format(prob))

        print('Сумма вероятностей подходящих выборок: {}'.format(sum(probs)))
        return sum(probs)


if __name__ == '__main__':
    row_ne, col_ne, samp_size = \
        eval(input('Введите через запятую равновесные вероятности строчного, столбцового игроков и размер '
                         'выборки.\n'))

    turn = 0
    while True:
        turn += 1
        print("Переход {}".format(turn))
        print('-' * 80)
        solver = StochasticPathSolver(float(row_ne), float(col_ne), int(samp_size))

        path_l, path_f = input('Введите предыдущее и последующее состояние первого (строчного) игрока через '
                               'запятую:\n').replace(' ', '').upper().split(sep=',')
        print('Для первого (строчного) игрока:')
        print('-' * 80)
        prob_row = solver.strategy_probability(path1=path_l, path2=path_f, mixed_ne_prob=row_ne)

        print()
        print('-' * 80)
        print()

        path_l, path_f = input('Введите предыдущее и последующее состояние второго (столбцового) игрока через '
                               'запятую:\n').replace(' ', '').upper().split(sep=',')
        print('Для второго (столбцового) игрока:')
        print('-' * 80)
        prob_col = solver.strategy_probability(path1=path_l, path2=path_f, mixed_ne_prob=col_ne)
        print('-' * 80)

        print('ВЕРОЯТНОСТЬ ПЕРЕХОДА: {}'.format(prob_row*prob_col))

        print()
        print('-' * 80)
        print('-' * 80)
        print()
